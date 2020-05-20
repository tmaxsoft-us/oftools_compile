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
from .Utils import Utils


class SetupJob(Job):

    def __init__(self, profile):
        self._profile = profile
        return

    def _analyze(self):

        # check if workdir is defined in the profile
        if self._profile.has_option('setup', 'workdir') is False:
            print('cannot find workdir section in the profile')
            exit(-1)

        # check if wordir accessable
        workdir = self._profile.get('setup', 'workdir')
        workdir = os.path.expandvars(workdir)
        if os.path.isdir(workdir) is False:
            if os.access(workdir, os.W_OK) is False:
                Log().get().critical('no write access on workdir = ' + workdir)
                exit(-1)

        return 0

    def _process_workdir(self, workdir, in_file):

        # Create the name for the workdir by adding suffix to in_file
        workdir = os.path.expandvars(workdir)
        try:
            file_name = in_file.rsplit('/', 1)[1]
        except:
            file_name = in_file

        cur_workdir = os.path.join(
            workdir, file_name + datetime.now().strftime("_%Y%m%d_%H%M%S"))

        # create_workdir
        if not os.path.isdir(cur_workdir):
            os.mkdir(cur_workdir)

        # copy source to workdir
        shutil.copy(in_file, cur_workdir)

        # change directory to workdir
        os.chdir(cur_workdir)

        # set log file handle
        Log().set_file('')

        return file_name

    def _process_env(self, key, value):
        Log().get().debug('key: ' + key)
        Log().get().debug('value: ' + value)

        env = Utils().get_env()
        env[key[1:]] = os.path.expandvars(value)
        Utils().set_env(env)

        return

    def run(self, in_file):

        Log().get().debug("Run SetupJob")
        out_file = ""

        # analyze setup section
        if self._profile.has_option('setup', 'workdir') is False:
            print('cannot find workdir section in the profile')
            exit(-1)

        # process setup section
        for key in self._profile.options('setup'):
            value = self._profile.get('setup', key)

            # handle workdir
            if key == "workdir":
                out_file = self._process_workdir(value, in_file)

            # handle environment variables
            elif key.startswith('$'):
                self._process_env(key, value)

        return out_file
