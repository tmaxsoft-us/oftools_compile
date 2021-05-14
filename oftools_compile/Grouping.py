#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""
# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context


class Grouping:
    """

    Attributes:
        _workdir_list:
        _group_dir:
        _group_log:

    Methods:
        __init():
        _create_group_dir():
        _group_logs_and_folders():
    """

    def __init__(self):
        """
        """
        self._workdir_list = Context().work_directories()
        self._group_dir = os.path.join(
            Context().root_workdir(),
            'group' + Context().tag() + Context().time_stamp())
        self._group_log = os.path.join(self._group_dir, 'group.log')

    def _create_group_dir(self):
        """
        """
        # Check if the group folder already exist
        if not os.path.isdir(self._group_dir):
            os.mkdir(self._group_dir)
        
        return 0

    def _group_logs_and_folders(self):
        """
        """
        with open(self._group_log, 'w') as group_log:

            for folder_path in self._workdir_list:
                file_list = os.listdir(folder_path)

                for file in file_list:
                    if file == 'oftools_compile.log':
                        # Retrieve absolute path of the current log file
                        file_path = os.path.join(folder_path, file)
                        with open(file_path, 'r') as oftools_compile_log:
                            # Read the log file and write to group log file
                            group_log.write(oftools_compile_log.read())
                
                # Move all compilation folders one by one
                shutil.move(folder_path, self._group_dir)

        return 0

    def run(self):
        """
        """
        self._create_group_dir()
        self._group_logs_and_folders()

        return 0
