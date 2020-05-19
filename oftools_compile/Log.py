#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import logging
import os
import time

# Third-party modules

# Owned modules


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log(object, metaclass=SingletonType):
    _logger = None
    _file_handler = None

    def __init__(self):
        self._logger = logging.getLogger("Logger")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s'
        )

        file_handler = logging.FileHandler("./oftools_compile.log")
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        self._file_handler = file_handler

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

    def __del__(self):
        self._file_handler.close()

    def info(self, msg):
        self._logger.info(msg)

    def error(self, msg):
        self._logger.error(msg)

    def get_logger(self):
        return self._logger