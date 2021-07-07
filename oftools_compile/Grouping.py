#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to group all working directories and aggregate the logs.

Typical usage example:
  grouping = Grouping()
  grouping.run()
"""
# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log


class Grouping(object):
    """A class used to group all working directory in on group directory, as well as aggregating all 
    compilation logs in one group log.

    Attributes:
        _workdir_list: A list, all the working directories created during the current execution of the 
            program.
        _group_directory: A string, the absolute path of the group directory.
        _group_log: A string, the absolute path of the group log.

    Methods:
        __init(): Initializes the class with all the attributes.
        _create_group_dir(): Run a mkdir command to create the group directory.
        _group_logs_and_folders(): Move the working directories to the group as well as log aggregation.
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
        """Run a mkdir command to create the group directory.

        Returns:
            An integer, the return code of the method.
        """
        # Check if the group folder already exist
        if not os.path.isdir(self._group_directory):
            Log().logger.debug('GROUPING: Creating group directory: ' +
                               self._group_directory)
            os.mkdir(self._group_directory)

        return 0

    def _group_logs_and_directories(self):
        """Move the working directories to the group as well as log aggregation.

        Returns:
            An integer, the return code of the method.
        """
        Log().logger.debug(
            'GROUPING: Moving working directories and aggregating logs')

        with open(self._group_log, 'w') as group_log:

            for directory_path in self._workdir_list:
                try:
                    file_list = os.listdir(directory_path)

                    for file in file_list:
                        if file == 'oftools_compile.log':
                            # Retrieve absolute path of the current log file
                            file_path = os.path.join(directory_path, file)
                            with open(file_path, 'r') as oftools_compile_log:
                                # Read the log file and write to group log file
                                group_log.write(oftools_compile_log.read())
                                group_log.write('\n\n')

                    # Move all compilation folders one by one
                    shutil.move(directory_path, self._group_directory)

                except FileNotFoundError:
                    Log().logger.warning(
                        'FileNotFoundError: No such file or directory:' +
                        directory_path + '. Skipping working directory')
                except shutil.Error as e:
                    Log().logger.warning(
                        'Error: ' + str(e) +
                        '. Skipping working directory move command')

        return 0

    def run(self):
        """General run method for the Grouping module.

        Returns:
            An integer, the return code of the method.
        """
        self._create_group_directory()
        self._group_logs_and_directories()

        return 0
