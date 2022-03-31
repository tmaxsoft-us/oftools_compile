#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to group all working directories and aggregate the logs.

Typical usage example:
  grouping = Grouping()
  grouping.run()
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Grouping(object):
    """A class used to group all working directory in on group directory, as well as aggregating all 
    compilation logs in one group log.

    Attributes:
        _workdir_list {list[string]} -- List of working directories created during the execution of the 
            program.
        _group_directory {string} -- Absolute path of the group directory.
        _group_log {string} -- Absolute path of the group log file.

    Methods:
        __init(): Initializes the class with all the attributes.
        _create_group_dir(): Runs a mkdir command to create the group directory.
        _group_logs_and_folders(): Moves the working directories to the group as well as performs log aggregation.
        run(): General run method for the Grouping module.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._workdir_list = Context().work_directories
        self._group_directory = os.path.join(
            Context().root_workdir,
            'group' + Context().tag + Context().time_stamp)
        self._group_log = os.path.join(self._group_directory, 'group.log')

        Context().group_directory = self._group_directory

    def _create_group_directory(self):
        """Runs a mkdir command to create the group directory.

        Returns:
            integer -- Return code of the method.
        """
        # Check if the group folder already exist
        Log().logger.debug(LogMessage.CREATE_GROUP_DIRECTORY.value %
                               self._group_directory)
        rc = FileHandler().create_directory(self._group_directory, 'group')

        return rc

    def _group_logs_and_directories(self):
        """Moves the working directories to the group as well as performs log aggregation.

        Returns:
            integer -- Return code of the method.
        """
        with open(self._group_log, 'w') as group_log:

            for directory_path in self._workdir_list:
                file_list = os.listdir(directory_path)

                for file_name in file_list:
                    if file_name == 'oftools_compile.log':
                        # Retrieve absolute path of the current log file
                        file_path = os.path.join(directory_path, file_name)
                        with open(file_path, 'r') as oftools_compile_log:
                            # Read the log file and write to group log file
                            Log().logger.debug(LogMessage.AGGREGATE_LOG_FILE.value)
                            group_log.write(oftools_compile_log.read())
                            group_log.write('\n\n')

                # Move all compilation folders one by one
                Log().logger.debug(LogMessage.MOVE_WORKING_DIRECTORY.value)
                FileHandler().move_directory(directory_path,
                                             self._group_directory)

        return 0

    def run(self):
        """General run method for the Grouping module.

        Returns:
            integer -- Return code of the method.
        """
        rc = self._create_group_directory()
        if rc != 0:
            return rc

        self._group_logs_and_directories()

        return rc
