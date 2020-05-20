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
    _formatter = None

    def __init__(self):
        self._logger = logging.getLogger("Logger")
        self._logger.setLevel(logging.INFO)
        self._formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s'
        )

        self._file_handler = logging.FileHandler("./oftools_compile.log")
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self._formatter)
        self._logger.addHandler(stream_handler)

    def __del__(self):
        self._file_handler.close()

    def set_file(self, file):
        if self._file_handler is not None:
            return

        self._file_handler = logging.FileHandler("./oftools_compile.log")
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)

    def set_level(self, level):
        if level == "DEBUG":
            self._logger.setLevel(logging.DEBUG)
        elif level == "INFO":
            self._logger.setLevel(logging.INFO)
        elif level == "WARNING":
            self._logger.setLevel(logging.WARNING)
        elif level == "ERROR":
            self._logger.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            self._logger.setLevel(logging.CRITICAL)

    def get(self):
        return self._logger