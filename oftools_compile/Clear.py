#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module can be used for test purposes, to clear all generated files and check only of the compilation process is running fine.

  Typical usage example:

  clear = Clear()
  clear.run()
"""

# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log


class Clear():
    """A class used to remove all generated files during compilation.

    Attributes:
        _workdir_list: A list, absolute path of working directories.
        _report_file_path: A string, absolute path of the report file generated during execution.

    Methods:
        __init__(grouping): Initializes the class with all the attributes.
        _clear_work_directories(): Removes all the working directories created during the given 
            execution.
        _clear_report_file(): Removes the report file from the report folder.
        run(): General run method to execute the clear option.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._workdir_list = Context().work_directories
        self._report_file_path = Context().report_file_path

    def _clear_work_directories(self):
        """Removes all the working directories created during the given execution.
        """
        if len(self._workdir_list) == 1:
            Log().logger.debug('CLEAR: Removing working directory')
        else:
            Log().logger.debug('CLEAR: Removing working directories one by one')
            
        for directory in self._workdir_list:
            shutil.rmtree(directory, ignore_errors=True)

    def _clear_report_file(self):
        """Removes the report file from the report folder.
        """
        try:
            Log().logger.debug('CLEAR: Removing report file')
            os.remove(self._report_file_path)
        except IsADirectoryError:
            Log().logger.debug('IsADirectoryError: Is a directory: ' +
                               self._report_file_path)
        except FileNotFoundError:
            Log().logger.debug(
                'FileNotFoundError: No such file or directory: ' +
                self._report_file_path)

    def run(self):
        """General run method to execute the clear option.
        """
        self._clear_work_directories()
        self._clear_report_file()

        return 0
