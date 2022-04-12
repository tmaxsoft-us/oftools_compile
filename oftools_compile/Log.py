#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to log all the events of the program execution.

Typical usage example:
  Log().open_stream()
  Log().set_level(args.log_level)
  Log().close_stream()
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
    """A class used to log all the events of the program execution.

    Attributes:
        _level_dict: A dictionary, associate a string and its corresponding log level from logging 
            module.
        _logger: A getLogger object.
        _formatter: A Formatter object, used to properly format log messages.
        _file_handler: A FileHandler object, to be able to write log messages to the current log file.
        _stream_handler: A StreamHandler object, to be able to write log messages to stdout.

    Methods:
        __init__(): Initializes the class with all the attributes.
        set_level(level): Changes log level based on user input.
        open_stream(): Opens the stream handler to write log messages to stdout.
        close_stream(): Closes the stream handler at the end of the program execution.
        open_file(path_to_file): Opens the file handler to write log messages to the log file.
        close_file(): Closes the file handler at the end of each file processing.

    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._level_dict = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self._level = ''

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        fmt = "%(asctime)-8s [%(levelname)-8s] %(message)s"
        self._formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")
        self._custom_formatter = CustomFormatter(fmt, datefmt="%H:%M:%S")

        self._file_handler = None
        self._stream_handler = None

    @property
    def logger(self):
        """Getter method for the attribute _logger.
        """
        return self._logger

    @property
    def level(self):
        """Getter method for the attribute _level
        """
        return self._level

    def set_level(self, level):
        """Changes log level based on user input.

        Args:
            level: A string, the user input for log level.
        """
        if level == 'DEBUG':
            fmt = "%(asctime)-8s [%(levelname)-8s] %(message)s (%(module)s:%(lineno)s)"
            self._formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")

        self._level = level
        self._logger.setLevel(self._level_dict[level])

    def open_stream(self):
        """Opens the stream handler to write log messages to stdout.
        """
        if self._stream_handler is None:
            self._stream_handler = logging.StreamHandler()
            self._stream_handler.setFormatter(self._custom_formatter)
            self._logger.addHandler(self._stream_handler)

    def close_stream(self):
        """Closes the stream handler at the end of the program execution.
        """
        if self._stream_handler is not None:
            self._logger.removeHandler(self._stream_handler)
            self._stream_handler.close()
            self._stream_handler = None

    def open_file(self, file_path):
        """Opens the file handler to write log messages to the log file.
        """
        if self._file_handler is None:
            self._file_handler = logging.FileHandler(filename=file_path,
                                                     mode='a',
                                                     encoding='utf-8')
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)

    def close_file(self):
        """Closes the file handler at the end of each file processing.
        """
        if self._file_handler is not None:
            self._logger.removeHandler(self._file_handler)
            self._file_handler.close()
            self._file_handler = None


class CustomFormatter(logging.Formatter):
    """
    """
    # DEBUG & INFO
    white = '\x1b[39m'
    # WARNING
    yellow = '\x1b[33m'
    # ERROR & CRITICAL
    red = '\x1b[91m'

    reset = '\x1b[0m'

    def __init__(self, fmt, datefmt):
        """
        """
        super().__init__()
        self.fmt = fmt
        self._date_fmt = datefmt
        self.FORMATS = {
            logging.DEBUG: self.white + self.fmt + self.reset,
            logging.INFO: self.white + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.red + self.fmt + self.reset
        }

    def format(self, record):
        """
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)