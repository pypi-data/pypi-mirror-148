import sys
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import IntEnum 
from datetime import datetime
from boltons.tbutils import ExceptionInfo

class Logger(IntEnum):
    NOTSET = 0
    DEBUG = 10 
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    EXCEPTION = 60


@dataclass_json
@dataclass
class MSGException:
    exc_type: str = ""
    value: str = ""
    traceback: BaseException = None

    def check(self):
        return self.traceback is None
    
    @property
    def info(self):
        einfo = ExceptionInfo.from_exc_info(exc_type, self.value, self.traceback)
        return einfo.to_dict()


    def __str__(self):
        return f"{self.exc_type} : {self.value}"
    
@dataclass_json
@dataclass
class MessageLog:
    func_name: str
    timestamp: datetime
    level: Logger
    message: str
    error: MSGException

    @property
    def msg(self):
        return f"{self.timestamp} :: {self.func_name} :: {self.message}"

    @property
    def exception(self):
        return self.error.check()   

    @property
    def exc(self):
        return self.error.info
    
    @property
    def log(self):
        return (self.level, self.msg)

    def __str__(self):
        return f"{self.func_name} :: {self.message} :: Error :> {self.exception}"

    @property
    def rdb(self):
        return {
            "function": self.func_name,
            "DT_GEN": self.timestamp, 
            "level": self.level, 
            "message": self.message, 
            "error": self.exc
        }
