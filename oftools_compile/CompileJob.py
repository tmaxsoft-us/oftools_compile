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
from .Context import Context


class CompileJob(Job):

    def _analyze(self, in_name):
        # check if given section is already completed
        if Context().is_section_complete('setup') is False:
            Log().get().error(
                'cannot proceed due to setup not being completed.')
            exit(-1)

        # check if given section is already completed
        if Context().is_section_complete(self._section):
            Log().get().debug('section has already been processed. skipping [' +
                              self._section + '] section.')
            return -1

        # evaluate filter to decide whether this section should run or not
        if self._evaluate_filter(self._section, in_name) is False:
            Log().get().debug('filter is False. skipping [' + self._section +
                              '] section.')
            return -1

        return 0

    def _process_option(self, in_name):
        option = ""

        try:
            option = self._profile.get(self._section, 'option')
        except:
            Log().get().warning('option not specified in the ' + self._section +
                                ' section.')

        # build command
        base_name = self._resolve_base_name(in_name)
        out_name = base_name + '.' + self._section
        #self._add_env('$OUTNAME', out_name)

        shell_cmd = self._resolve_section_base(self._section) + " "
        shell_cmd += option
        #shell_cmd = os.path.expandvars(shell_cmd)
        shell_cmd = shell_cmd.replace("$INNAME", in_name)
        shell_cmd = shell_cmd.replace("$OUTNAME", out_name)

        # run command
        Log().get().info("shell_cmd: " + shell_cmd)
        env = Context().get_env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()

        # handle error
        if proc.returncode != 0:
            Log().get().error(self._section + ' error detected')
            Log().get().error(out.decode('utf-8'))
            Log().get().error(err.decode('utf-8'))
            exit(proc.returncode)

        return out_name

    def run(self, in_name):
        # analyze section
        if self._analyze(in_name) < 0:
            Log().get().info("[" + self._section + "] skip section")
            return in_name

        # start section
        Log().get().info("[" + self._section + "] start section")

        # add environment variables
        for key in self._profile.options(self._section):
            value = self._profile.get(self._section, key)

            if key.startswith('$'):
                self._add_env(key, value)

        # process option
        key = self._profile.get(self._section, 'option')
        out_name = self._process_option(in_name)
        if os.path.isfile(out_name) is not True:
            out_name = in_name

        # set section as completed
        Context().set_section_complete(self._section)

        # end section
        Log().get().info("[" + self._section + "] end section")

        return out_name
