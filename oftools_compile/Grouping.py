#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the module in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context


class Grouping:

    def __init__(self):
        self._workdir_list = Context().get_workdir_list()
        self._group_dir = os.path.join(
            Context().get_root_workdir(),
            'group' + Context().get_const_tag() + Context().get_time_stamp())
        self._concatenation_log = os.path.join(self._group_dir, 'group.log')

    def _merge_logs(self):

        # Check if the grouping folder already exist
        if not os.path.isdir(self._group_dir):
            os.mkdir(self._group_dir)

        with open(self._concatenation_log, 'w') as master_log:
            for path_to_folder in self._workdir_list:
                file_list = os.listdir(path_to_folder)
                for file in file_list:
                    if 'oftools_compile.log' in file:
                        # Retrieve absolute path of the current log file
                        path_to_file = os.path.join(path_to_folder, file)
                        with open(path_to_file, 'r') as single_log:
                            # Read the log file and write to master log file
                            master_log.write(single_log.read())

        return 0

    def _grouping_folders(self):

        # Move all compilation folders one by one
        for path_to_folder in self._workdir_list:
            shutil.move(path_to_folder, self._group_dir)

        return 0

    def run(self):

        self._merge_logs()
        self._grouping_folders()

        return 0
