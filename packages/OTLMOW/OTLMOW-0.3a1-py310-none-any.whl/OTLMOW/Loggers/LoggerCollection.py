from OTLMOW.Loggers.AbstractLogger import AbstractLogger
from OTLMOW.Loggers.LogType import LogType


class LoggerCollection(AbstractLogger):
    def __init__(self, listOfLoggers):
        self.listOfLoggers = listOfLoggers

    def log(self, message, logType: LogType):
        if type(self.listOfLoggers) is list:
            logger:AbstractLogger
            for logger in self.listOfLoggers:
                logger.log(message, logType)
