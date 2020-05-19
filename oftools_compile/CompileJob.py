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


class CompileJob(Job):

    def __init__(self, section, config):
        self._section = section
        self._config = config
        return

    def run(self, in_file):
        Log().info("Run CompileJob")
        Log().info("in_file: " + in_file)

        # build command
        option = self._config.get(self._section, 'option')
        base_name = self.get_base_name(in_file)
        out_file = base_name + '.' + self._section

        shell_cmd = self._section + " "
        shell_cmd += option
        shell_cmd += ' -o ' + out_file + ' ' + in_file

        # run command
        Log().info("Command: " + shell_cmd)
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
        out, err = proc.communicate()

        # handle resultget
        if proc.returncode != 0:
            Log().error(self._section + ' error detected')
            Log().error(out.decode('utf-8'))
            Log().error(err.decode('utf-8'))
            exit(proc.returncode)

        Log().info("out_file: " + out_file)

        return out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]