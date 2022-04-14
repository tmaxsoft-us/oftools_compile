#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module can be used for test purposes, to clear all generated files and check only of the 
compilation process is running fine.

  Typical usage example:

  clear = Clear()
  clear.run()
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Clear(object):
    """A class used to remove all generated files during compilation.

    Attributes:
        _working_directory_list {list} -- Absolute path of working directories.
        _report_file_path {string} -- Absolute path of the report file generated during execution.

    Methods:
        __init__(grouping) -- Initializes the class with all the attributes.
        _clear_work_directories() -- Removes all the working directories created during the given 
            execution.
        _clear_report_file() -- Removes the report file from the report folder.
        run() -- General run method to execute the clear option.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._working_directory_list = Context().work_directories
        self._report_file_path = Context().report_file_path

    def _clear_working_directories(self):
        """Removes all the working directories created during the given execution.
        """
        Log().logger.debug(LogMessage.CLEAR_WORKING_DIRECTORY.value)

        for directory in self._working_directory_list:
            FileHandler().delete_directory(directory)

    def _clear_report_file(self):
        """Removes the report file from the report folder.
        """
        Log().logger.debug(LogMessage.CLEAR_REPORT_FILE.value %
                           self._report_file_path)
        FileHandler().delete_file(self._report_file_path)

    def run(self):
        """General run method to execute the clear option.
        """
        self._clear_working_directories()
        self._clear_report_file()

        return 0
