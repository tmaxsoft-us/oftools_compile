#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import shutil
from datetime import datetime

# Third-party modules

# Owned modules
from .Log import Log
from .Job import Job


class SetupJob(Job):

    def __init__(self, config):
        self._config = config
        return

    def run(self, in_file):

        # resolve work dir
        if self._config.has_option('setup', 'workdir') is False:
            print('cannot find workdir section in the profile')
            exit(-1)
        workdir = os.path.expandvars(self._config.get('setup', 'workdir'))
        if os.path.isdir(workdir) is False:
            print('work dir not valid = ' + workdir)
            exit(-1)

        # Create the name for the workdir by adding suffix to in_file
        try:
            file_name = in_file.rsplit('/', 1)[1]
        except:
            file_name = in_file

        time_stamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
        in_file_time = file_name + time_stamp
        cur_workdir = os.path.join(workdir, in_file_time)

        # create_workdir
        if not os.path.isdir(cur_workdir):
            os.mkdir(cur_workdir)

        # copy source to workdir
        shutil.copy(in_file, cur_workdir)

        # change directory to workdir
        os.chdir(cur_workdir)

        out_file = file_name

        # Create logger object
        Log().info("Run SetupJob")
        Log().info('create directory ' + cur_workdir)
        Log().info("SetupJob Completed")

        return out_file
