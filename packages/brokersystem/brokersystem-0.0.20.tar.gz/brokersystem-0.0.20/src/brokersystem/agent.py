from re import A
import threading
import json, traceback, time, importlib, sys
import pandas as pd
import requests
from logzero import logger
import os, glob, importlib



class ValueTemplate:
    def __init__(self, unit=None):
        self.type = self.__class__.__name__.lower()
        self.unit = unit
        self.constraint_dict = {}
        self.constraint_dict = {}
        self.item_type = None
    
    def set_constraint(self, key, value):
        if value is not None:
            self.constraint_dict[key] = value
    
    @property
    def format_dict(self):
        format = {"@type": self.type, "@unit": self.unit}
        if self.item_type == "input":
            format.update({"@necessity": "required","@constraints": self.constraint_dict})
        if self.item_type == "output":
            format.update({})
        return format

    def cast(self, value):
        return value

    def format_for_output(self, value):
        format_dict = {"@type": self.type, "@unit": self.unit}
        return value, format_dict
    
    def set_item_type(self, item_type):
        self.item_type = item_type

class Number(ValueTemplate):
    def __init__(self, value=None, unit=None, min=None, max=None):
        super().__init__(unit)
        self.set_constraint("default", value)
        self.set_constraint("min", min)
        self.set_constraint("max", max)
    
    def cast(self, value):
        try:
            value = int(value)
        except:
            value = float(value)
        assert not ("min" in self.constraint_dict and value < self.constraint_dict["min"])
        assert not ("max" in self.constraint_dict and value > self.constraint_dict["max"])
        return value

class Range(ValueTemplate):
    def __init__(self, range_min=None, range_max=None, unit=None):
        super().__init__(unit)
        self.set_constraint("default", {"min": range_min, "max": range_max})

class String(ValueTemplate):
    def __init__(self, string=None):
        super().__init__()
        self.set_constraint("default", string)

class File(ValueTemplate):
    def __init__(self, file_type=None):
        super().__init__()
        self.set_constraint("file_type", file_type)

class Choice(ValueTemplate):
    def __init__(self, choices: list, unit=None):
        super().__init__(unit)
        self.set_constraint("choices", choices)

    def cast(self, value):
        try:
            value = int(value)
        except:
            pass
        try:
            value = float(value)
        except:
            pass
        assert value in self.constraint_dict["choices"]
        return value

class Table(ValueTemplate):
    def __init__(self, unit_dict:dict, graph:dict=None):
        super().__init__(unit=None)
        self.unit_dict = unit_dict.copy()
        self.graph = graph


    def cast(self, value):
        return value

    @property
    def format_dict(self):
        format_dict = super().format_dict
        format_dict["@table"] = list(self.unit_dict.keys())
        return format_dict

    def format_for_output(self, value):
        if self.graph is not None:
            format_dict = {"@type": self.type, "@ui": {"type": "graph", "key_x": self.graph["x"], "key_y": self.graph["y"]}, "_unit_dict": self.unit_dict}
            if isinstance(value, pd.DataFrame):
                value = value.to_dict(orient="list")
            else:
                raise 
        return value, format_dict
            

class TemplateContainer:
    def __init__(self, item_type):
        self._container_dict = {}
        self._value_keys = []
        self._table_keys = []
        self._item_type = item_type

    def __setattr__(self, key: str, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
            return
        if not isinstance(value, ValueTemplate):
            logger.error(f"You can only set ValueTemplate object(such as Number or Table) for input, condition and output: {key} ({type(value)})")
            return
        self._container_dict[key] = value
        if isinstance(value, Table):
            if key not in self._table_keys:
                self._table_keys.append(key)
        elif key not in self._value_keys:
            self._value_keys.append(key)
        value.set_item_type(self._item_type)
    
    def _get_template(self, item_type):
        if item_type == "input":
            format_keys = ["@type", "@unit", "@necessity", "@constraints"]
        if item_type == "output":
            format_keys = ["@type", "@unit", "@ui"]
        if item_type == "condition":
            format_keys = ["@type", "@unit", "@value"]
        template_dict = {fkey: {} for fkey in format_keys}

        template_dict["@keys"] = self._value_keys + self._table_keys
        if len(self._value_keys) > 0:
            template_dict["@value"] = self._value_keys.copy()

        if len(self._table_keys) > 0:
            template_dict["@table"] = {} # will be given by Table instance


        for key, template in self._container_dict.items():
            for fkey, fvalue in template.format_dict.items():
                assert key not in template_dict[fkey], f"Duplicated key error: {key}"
                template_dict[fkey][key] = fvalue
        return template_dict
    
    def __contains__(self, key):
        return key in self._container_dict
    
    def __getitem__(self, key):
        return self._container_dict[key]

class ValueContainer:
    def __init__(self, value_dict):
        self._container_dict = value_dict.copy()

    def __getattr__(self, key: str):
        if key.startswith("_"):
            return super().__getattr__(key)
        return self._container_dict[key]
    
    def __getitem__(self, key: str):
        return self._container_dict[key]


class AgentInterface:
    def __init__(self):
        self.secret_token = ""
        self.name = None
        self.charge = 10000
        self.convention = ""
        self.description = ""
        self.input = TemplateContainer("input")
        self.condition = TemplateContainer("condition")
        self.output = TemplateContainer("output")
    
    def prepare(self, func_dict):
        self.func_dict = func_dict.copy()
        if "make_config" not in self.func_dict and (self.secret_token == "" or self.name == None):
            logger.error("Secret_token and name should be specified.")
            return
        if "job_func" not in self.func_dict:
            logger.error("job execution function is required: Prepare a decorated function with @job_func.")
            return
        self.make_config()

    def make_config(self, for_registration=False):
        if "make_config" in self.func_dict:
            self.func_dict["make_config"]()
            if self.name is None:
                logger.error("Agent's name should be set in config function")
        config_dict = {}
        for item_type in ["input", "condition", "output"]:
            config_dict[item_type] = getattr(getattr(self, item_type), "_get_template")(item_type)
        
        config_dict["charge"] = self.charge
        if for_registration:
            config_dict["module_version"] = __version__ if "__version__" in globals() else "-1.0.0"
            config_dict["convention"] = self.convention
            config_dict["description"] = self.description

        return config_dict
    
    def has_func(self, func_name):
        return func_name in self.func_dict
    
    def validate(self, input_dict):
        template_dict = self.input._get_template("input")
        msg = "ok"
        for key in template_dict["@keys"]:
            if key in input_dict:
                try:
                    value = self.input[key].cast(input_dict[key])
                    template_dict[key] = value
                except [AssertionError, TypeError]:
                    msg = "need_revision"
        return msg, template_dict

    def cast(self, key, input_value):
        if key not in self.input:
            logger.error(f"{key} is not registered as input.")
            raise Exception
        return self.input[key].cast(input_value)
    
    def format_for_output(self, result_dict):
        output_dict = {"@unit": {}, "@type": {}, "@option": {}, "@ui": {}, "@keys": []}

        for key, value in result_dict.items():
            if key not in self.output:
                continue
            output_value, format_dict = self.output[key].format_for_output(value)
            if output_value is None:
                continue
            output_dict[key] = output_value
            output_dict["@keys"].append(key)
            ### manage type specific properties 
            if format_dict["@type"] == "table":
                if "@table" not in output_dict:
                    output_dict["@table"] = {}
                table_keys = list(format_dict["_unit_dict"].keys())
                output_dict["@unit"].update(format_dict["_unit_dict"])
                output_dict["@type"].update({k: "number" for k in table_keys})
                output_dict["@table"][key] = table_keys
            else:
                if "@value" not in output_dict:
                    output_dict["@value"] = []
                output_dict["@value"].append(key)

            for fk, fv in format_dict.items():
                if not fk.startswith("_"):
                    output_dict[fk][key] = fv
        # remove empty property keys
        
        return output_dict

class Job:
    def __init__(self, agent, negotiation_id, request):
        self._agent = agent
        self._negotiation_id = negotiation_id
        self._request = request
        self._result_dict = {}
    
    def report(self, msg=None, progress=None, result=None):
        payload =  {"negotiation_id": self._negotiation_id, "status": self._agent.status}
        if msg is not None:
            payload["msg"] = msg
        if progress is not None:
            payload["progress"] = progress
        if result is not None:
            assert isinstance(result, dict), "Result should be given as a dict: {result_key: result_value}"
            self._result_dict.update(result)
            payload["result"] = self._agent.interface.format_for_output(self._result_dict)

        self._agent.post("report", payload)

    def msg(self, msg):
        self.report(msg=msg)
    
    def progress(self, progress, msg=None):
        self.report(progress=progress, msg=msg)
        
    def __getitem__(self, key):
        return self._agent.interface.cast(key, self._request[key])

class Agent:
    RESTART_INTERVAL_CRITERIA = 30
    HEARTBEAT_INTERVAL = 2
    
    def __init__(self, broker_url):
        self._to_show_i_am_agent_instance = True
        self.broker_url = broker_url
        self.agent_funcs = {}
        self.running = False
        self.interface = AgentInterface()

    def run(self):
        if self.running:
            return
        self.interface.prepare(self.agent_funcs)
        self.auth = self.interface.secret_token
        self.status = "init"
        self.polling_interval = 0
        self.last_heartbeat = time.time()
        if self.register_config():
            self.running = True
            threading.Thread(target=self.connect, daemon=True).start()
            threading.Thread(target=self.heartbeat).start()
            if not _check_if_batch_mode_is_on():
                logger.info(f"Agent {self.interface.name} has started. Press return to quit.")
                input("")
                self.goodbye()

    def goodbye(self):
        self.running = False
    
    def register_config(self):
        for _ in range(5):
            response = self.post("config", self.interface.make_config(for_registration=True))
            if "status" in response and response["status"] == "ok":
                logger.info(f"Agent {self.interface.name} has successfully connected to the broker system!")
                return True
            else:
                logger.warning("Cannot connect to the broker system.")
            time.sleep(3)
        logger.error("Stop try connecting to the broker system.")
        return False

    def heartbeat(self):
        restart_timer = None
        while self.running:
            if time.time() - self.last_heartbeat > self.RESTART_INTERVAL_CRITERIA:
                if restart_timer is None:
                    restart_timer = time.time()
                elif time.time() - restart_timer >= self.RESTART_INTERVAL_CRITERIA:
                    restart_timer = None
                    logger.info(f"Automatic reconnection...")
                    threading.Thread(target=self.connect, daemon=True).start()
            else:
                restart_timer = None
            time.sleep(self.HEARTBEAT_INTERVAL)

    def connect(self):
        first_time_flag = True
        while self.running:
            self.last_heartbeat = time.time()
            try:
                messages = self.check_msgbox()
                if first_time_flag:
                    first_time_flag = False
                    
                if len(messages) > 0:
                    logger.debug(f"Number of messages: {len(messages)}")
                for message in messages:
                    threading.Thread(target=self.process_message, args=[message], daemon=True).start()
            except Exception:
                logger.exception(traceback.format_exc())
            time.sleep(self.polling_interval)

    def check_msgbox(self):
        response = self.get(f"msgbox")
        if len(response) > 0:
            logger.debug(f"CHECK_MSGBOX {response}")
            return response["messages"]
        return []

    def process_message(self, message):
        try:
            logger.debug(f"Message: {message}")
            if "msg_type" not in message or "body" not in message:
                logger.exception(f"Wrong message format: {message}")
                return
            if message["msg_type"] == "negotiation_request":
                self.process_negotiation_request(message["body"])
            if message["msg_type"] == "negotiation":
                self.process_negotiation(message["body"])
            if message["msg_type"] == "contract":
                self.process_contract(message["body"])
        except:
            logger.exception(traceback.format_exc())

    def process_negotiation_request(self, msg):
        negotiation_id = msg["negotiation_id"]
        response = self.interface.make_config()
        msg = "need_revision"
        self.post("negotiation/response", {"msg": msg, "negotiation_id": negotiation_id, "response": response})

    def process_negotiation(self, msg):
        negotiation_id = msg["negotiation_id"]
        response = self.interface.make_config()
        msg, input_response = self.interface.validate(msg["request"])
        response["input"] = input_response
        if msg == "ok" and self.interface.has_func("negotiation"):
            msg, response = self.interface.func_dict["negotiation"](msg["request"], response)
            if msg not in ["ok", "need_revision", "ng"]:
                logger.exception(f"Negotation func in {self.interface.name} returns a wrong msg: should be one of 'ok', 'need_revision' or 'ng'")
            if msg in ["ok", "ng"]:
                response = {}    
        logger.debug(f"MSG {msg} RESPONSE {response}")
        self.post("negotiation/response", {"msg": msg, "negotiation_id": negotiation_id, "response": response})

    def process_contract(self, msg):
        negotiation_id = msg["negotiation_id"]
        request = msg["request"]
        job = Job(self, negotiation_id, request)
        try:
            self.post("contract/accept", {"negotiation_id": negotiation_id})
            self.status = "running"
            job.msg(f"{self.interface.name} starts running...")
        
            result = self.interface.func_dict["job_func"](job)
            logger.debug(f"JOB RETURN VALUE: {result}")
            if result is None:
                result = {}
            self.status = "done"
            job.report(msg="Job done.", progress=1, result=result)
        except:
            logger.exception(traceback.format_exc())
            self.status = "error"
            job.report(msg="Error occured during the job.", progress=-1)
       
    
    @property
    def header(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers.update({"authorization": f"Basic {self.auth}"})

        return headers

    def post(self, uri, payload):
        try:
            response = requests.post(f"{self.broker_url}/api/v1/agent/{uri}", json=payload, headers=self.header)
        except requests.exceptions.ConnectionError:
            return {}
        if response.status_code != 200:
            logger.exception(response.status_code)
            return {}
        return response.json()

    def get(self, uri):
        try:
            response = requests.get(f"{self.broker_url}/api/v1/agent/{uri}", headers=self.header)
        except requests.exceptions.ConnectionError:
            if self.polling_interval < 10:
                self.polling_interval += 1
            return {}

        if response.status_code != 200:
            logger.exception(response.status_code)
            if self.polling_interval < 10:
                self.polling_interval += 1
            return {}
        self.polling_interval = 0
        return response.json()

    def register_func(self, func_name, func):
        self.agent_funcs[func_name] = func

    ##### wrapper functions #####
    def config(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("make_config", wrapper)
        return wrapper

    def negotiation(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("negotiation", wrapper)
        return wrapper

    def job_func(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        self.register_func("job_func", wrapper)
        return wrapper
    
    ##### interface for agent interface #####
    @property
    def input(self):
        return self.interface.input
    @property
    def output(self):
        return self.interface.output
    @property
    def condition(self):
        return self.interface.condition
    @property
    def secret_token(self):
        return self.interface.secret_token
    @secret_token.setter
    def secret_token(self, token):
        self.interface.secret_token = token
    @property
    def name(self):
        return self.interface.name
    @name.setter
    def name(self, name):
        self.interface.name = name
    @property
    def convention(self):
        return self.interface.convention
    @convention.setter
    def convention(self, convention):
        self.interface.convention = convention
    @property
    def description(self):
        return self.interface.description
    @description.setter
    def description(self, description):
        self.interface.description = description
    @property
    def charge(self):
        return self.interface.charge
    @charge.setter
    def charge(self, charge):
        self.interface.charge = charge
    

class Broker:
    def __init__(self, job = None, broker_url=None, auth=None):
        if job is None:
            assert broker_url is not None and auth is not None
            self.broker_url = broker_url
            self.auth = auth
        elif isinstance(job, Job):
            self.broker_url = job._agent.broker_url
            self.auth = job._agent.interface.secret_token
        else:
            raise Exception

    def ask(self, agent_id, request):
        response = self.negotiate(agent_id, request)
        negotiation_id = response["negotiation_id"]
        self.contract(negotiation_id)
        result = self.get_result(negotiation_id)
        return result

    def negotiate(self, agent_id, request):
        response = self.post("negotiate", {"agent_id": agent_id, "request": request})
        return response

    def contract(self, negotiation_id):
        response = self.post("contract", {"negotiation_id": negotiation_id})
        return response

    def get_result(self, negotiation_id):
        msg = ""
        while True:
            response = self.get(f"result/{negotiation_id}")
            if response["msg"] != msg:
                msg = response["msg"]
                logger.debug(msg)
            if response["status"] in ["done", "error"]:
                break
            time.sleep(1)
        return response

    @property
    def header(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        headers.update({"authorization": f"Basic {self.auth}"})
        return headers

    def post(self, uri, payload):
        try:
            logger.debug
            response = requests.post(f"{self.broker_url}/api/v1/client/{uri}", json=payload, headers=self.header)
        except requests.exceptions.ConnectionError:
            logger.exception(traceback.format_exc())
        if response.status_code != 200:
            logger.exception(response.status_code)
            return {}
        return response.json()

    def get(self, uri):
        try:
            response = requests.get(f"{self.broker_url}/api/v1/client/{uri}", headers=self.header)
        except requests.exceptions.ConnectionError:
            logger.exception(traceback.format_exc())
            return {}

        if response.status_code != 200:
            logger.exception(response.status_code)
            return {}
        return response.json()
    


# def run(broker_url):
#     if not _check_if_batch_mode_is_on():
#         agent = Agent(broker_url)
#         if agent.running:
#             logger.info(f"Agent {agent.interface.name} has started. Press return to quit.")
#             input("")
#             agent.goodbye()
    


class AgentManager:
    WATCHING_INTERVAL = 5
    broker_url = None
    def __init__(self, broker_url, dir_path=""):
        self.broker_url = broker_url
        self.dir_path = dir_path
        self.agents = {}
        self.start_watching_loop()
    
    def start_watching_loop(self):
        while True:
            try:
                self.dog_watching()
                time.sleep(self.WATCHING_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Automatic agent runner closing...")
                break
        for k in self.agents.keys():
            self.stop(k)

    def dog_watching(self):
        exisiting_files = set(glob.glob(os.path.join(self.dir_path, "*.py"), recursive=True))
        current_files = set(self.agents.keys())
        new_files = exisiting_files - current_files
        removed_files = current_files - exisiting_files
        ongoing_files = current_files & exisiting_files
        for file in new_files:
            self.load(file)
        for file in ongoing_files:
            self.check_for_update(file)
        for file in removed_files:
            self.stop(file)
            self.agents.pop(file)
    
    def run_module(self, module):
        def is_agent(obj):
            return hasattr(obj, "_to_show_i_am_agent_instance")
        for key in module.__dir__():
            if is_agent(getattr(module, key)):
                agent = getattr(module, key)
                agent.run()
                return agent
        return None

    def load(self, file):
        self.agents[file] = {"mtime": os.path.getmtime(file)}
        try:
            module_name = file.replace(".py", "").replace(os.path.sep, ".")
            module = importlib.import_module(module_name)
            self.agents[file]["module"] = module
            agent = self.run_module(module)
            if agent is not None:
                self.agents[file]["agent"] = agent
                logger.info(f"Agent {agent.interface.name} has started!")
        except:
            logger.exception(traceback.format_exc())

    def check_for_update(self, file):
        try:
            if os.path.getmtime(file) != self.agents[file]["mtime"]:
                self.agents[file]["mtime"] = os.path.getmtime(file)
                if "module" not in self.agents[file]:
                    self.load(file)
                    return
                if "agent" in self.agents[file]:
                    self.agents[file]["agent"].goodbye()
                    time.sleep(Agent.HEARTBEAT_INTERVAL)
                    
                module = importlib.reload(self.agents[file]["module"])
                self.agents[file]["module"] = module
                agent = self.run_module(module)
                if agent is not None:
                    self.agents[file]["agent"] = agent
                    logger.info(f"Agent {agent.interface.name} has started!")
        except:
            logger.exception(traceback.format_exc())
    
    def stop(self, file):
        try:
            if "agent" in self.agents[file]:
                self.agents[file]["agent"].goodbye()
        except:
            logger.exception(traceback.format_exc())

def _check_if_batch_mode_is_on():
    return len(sys.argv) >= 2 and ("http://" in sys.argv[1] or "https://" in sys.argv[1])

def batch_run():
    if _check_if_batch_mode_is_on():
        AgentManager(sys.argv[1])
    else:
        logger.warning("Put the broker url as a first argument to make the automatic mode work.")

if __name__ == "__main__":
    batch_run()