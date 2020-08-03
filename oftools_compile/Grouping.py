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
        self._root_workdir = Context().get_root_workdir()
        self._group_dir = os.path.join(self._root_workdir, 'group' + Context().get_const_tag() + Context().get_time_stamp())
        self._concatenation_log = os.path.join(self._group_dir, 'group.log')

    def _grouping_folders(self):
        
        # Check if the grouping folder already exist
        if not os.path.isdir(self._group_dir):
            os.mkdir(self._group_dir)

        # Move all compilation folders one by one
        for folder in next(os.walk(self._root_workdir))[1]:
            if ((Context().get_const_tag() and Context().get_time_stamp()) in folder) and ('group' not in folder):
                # Retrieve absolute path of the current compilation folder
                path_to_folder = os.path.join(self._root_workdir, folder)
                # Move this folder under the grouping directory
                shutil.move(path_to_folder, self._group_dir)
        
        return 0


    def _merge_logs(self):

        with open(self._concatenation_log, 'w') as master_log: 
            for root, _, files in os.walk(self._group_dir):
                for log in files:
                    # Search all files names oftools_compile.log
                    if ('oftools_compile.log' in log):
                        # Retrieve absolute path of the current log file
                        path_to_file = os.path.join(root, log)
                        with open(path_to_file, 'r') as single_log:
                            # Read the log file and write to master log file
                            master_log.write(single_log.read())

        return 0

    def run(self):

        self._grouping_folders()
        self._merge_logs()

        return 0
        