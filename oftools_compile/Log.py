#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import logging

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
    """

    Attributes:
        _level_dict:
        _logger:
        _formatter:
        _file_handler:
        _stream_handler:

    Methods:
        __init__():
        set_level(level):
        open_stream():
        close_stream():
        open_file(path_to_file):
        close_file():

    """

    def __init__(self):
        """
        """
        self._level_dict = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        self._formatter = logging.Formatter(
            fmt="%(asctime)-8s [%(levelname)8s] %(message)s",
            datefmt="%H:%M:%S")

        self._file_handler = None
        self._stream_handler = None

    @property
    def logger(self):
        """
        """
        return self._logger

    def set_level(self, level):
        """
        """
        if level == 'DEBUG':
            self._formatter = logging.Formatter(
                fmt=
                "%(asctime)-8s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
                datefmt="%H:%M:%S")
        self._logger.setLevel(self._level_dict[level])

    def open_stream(self):
        """
        """
        if self._stream_handler == None:
            self._stream_handler = logging.StreamHandler()
            self._stream_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._stream_handler)

    def close_stream(self):
        """
        """
        if self._stream_handler != None:
            self._logger.removeHandler(self._stream_handler)
            self._stream_handler.close()
            self._stream_handler = None

    def open_file(self, file_path):
        """
        """
        if self._file_handler == None:
            self._file_handler = logging.FileHandler(filename=file_path,
                                                     mode='a',
                                                     encoding='utf-8')
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)

    def close_file(self):
        """
        """
        if self._file_handler != None:
            self._logger.removeHandler(self._file_handler)
            self._file_handler.close()
            self._file_handler = None
