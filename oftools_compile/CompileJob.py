#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import subprocess
import shutil
import os

# Third-party modules

# Owned modules
from .Job import Job
from .Log import Log
from .Utils import Utils


class CompileJob(Job):

    def __init__(self, section, profile):
        self._section = section
        self._profile = profile
        return

    def _process_option(self):
        option = ""

        try:
            option = self._profile.get(self._section, 'option')
        except:
            Log().get().warning('option not specified in the ' + self._section +
                                ' section.')

        return option

    def _process_filter(self):

        shell_cmd = ""

        try:
            shell_cmd = self._profile.get(self._section, 'filter')
        except:
            return True

        Log().get().info("run command: " + shell_cmd)
        env = Utils().get_env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()
        Log().get().debug(out.decode('utf-8'))

        # grep returns 0 if line matches
        if proc.returncode == 0:
            return True

        return False

    def run(self, in_file):
        Log().get().debug("Run CompileJob")
        Log().get().debug("in_file: " + in_file)

        # process profile defined options
        option = self._process_option()
        filter = self._process_filter()

        # skip if filter condition does not match
        if filter is False:
            Log().get().debug('filter is False. skipping [' + self._section +
                              '] section.')
            return in_file

        # build command
        base_name = self.get_base_name(in_file)
        out_file = base_name + '.' + self._section

        shell_cmd = self._section + " "
        shell_cmd += option
        shell_cmd = shell_cmd.replace("$INNAME", in_file)
        shell_cmd = shell_cmd.replace("$OUTNAME", out_file)

        # run command
        Log().get().info("run command: " + shell_cmd)
        env = Utils().get_env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()
        Log().get().info(out.decode('utf-8'))

        # handle error
        if proc.returncode != 0:
            Log().get().error(self._section + ' error detected')
            Log().get().error(err.decode('utf-8'))
            exit(proc.returncode)

        # do not change file if there is no new file generated
        if os.path.isfile(out_file) is not True:
            out_file = in_file

        Log().get().debug("out_file: " + out_file)

        return out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]