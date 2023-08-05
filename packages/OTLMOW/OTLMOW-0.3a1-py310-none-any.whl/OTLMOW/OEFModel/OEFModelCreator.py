from datetime import datetime

from OTLMOW.Loggers.AbstractLogger import AbstractLogger
from OTLMOW.Loggers.LogType import LogType
from OTLMOW.OEFModel.OEFClassCreator import OEFClassCreator


class OEFModelCreator:
    def __init__(self, logger: AbstractLogger, classes: [dict], attributen: [dict]):
        self.logger = logger
        self.classes = classes
        self.attributen = attributen
        self.logger.log("Created an instance of OEFModelCreator", LogType.INFO)

    def create_full_model(self):
        self.logger.log('started creating model at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), logType=LogType.INFO)
        self.create_classes()
        self.logger.log('finished creating model at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), logType=LogType.INFO)

    def create_classes(self):
        creator = OEFClassCreator(self.logger, self.attributen)

        for cls in self.classes:
            try:
                dataToWrite = creator.create_block_to_write_from_class(cls)
                if dataToWrite is None:
                    self.logger.log(f"Could not create a class for {cls['naam']}", LogType.INFO)
                    pass
                if len(dataToWrite) == 0:
                    self.logger.log(f"Could not create a class for {cls['naam']}", LogType.INFO)
                    pass
                creator.writeToFile(cls, relativePath='Classes', dataToWrite=dataToWrite)
                self.logger.log(f"Created a class for {cls['naam']}", LogType.INFO)
            except Exception as e:
                self.logger.log(str(e), LogType.ERROR)
                self.logger.log(f"Could not create a class for {cls['naam']}", LogType.ERROR)
