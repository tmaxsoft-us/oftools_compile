import logging
import os
import time

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class MyLogger(object, metaclass=SingletonType):
    _logger = None
    _fileHandler = None
    _streamHandler = None

    def __init__(self):
        self._logger = logging.getLogger("Logger")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        self._fileHandler = logging.FileHandler("./oftools_compile.log")
        self._streamHandler = logging.StreamHandler()

        self._fileHandler.setFormatter(formatter)
        self._streamHandler.setFormatter(formatter)

        self._logger.addHandler(self._fileHandler)
        self._logger.addHandler(self._streamHandler)

        print ("Generate New Logger Instance")

    def get_logger(self):
        return self._logger

    def __del__(self):
        self._fileHandler.close()
        self._streamHandler.close()
        return
