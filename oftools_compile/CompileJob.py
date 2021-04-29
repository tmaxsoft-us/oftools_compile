#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import subprocess
import os

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class CompileJob(Job):
    """
    
    Methods:
        _analyze(in_name):
        _process_option():
    """

    def _analyze(self, in_name):
        # Check if given section is already completed
        if Context().is_section_complete('setup') is False:
            Log().logger.error(
                'cannot proceed due to setup not being completed.')
            exit(-1)

        # check if given section is already completed
        if Context().is_section_complete(self._section):
            Log().logger.debug('section has already been processed. skipping [' +
                              self._section + '] section.')
            return -1

        # evaluate filter to decide whether this section should run or not
        if self._profile.evaluate_filter(self._section, in_name) is False:
            Log().logger.debug('[' + self._section + '] ' +
                              self._profile.resolve_filter(self._section) +
                              ' is False. skipping section.')
            return -1

        return 0

    def _process_option(self):
        option = ""

        try:
            option = self._profile.get(self._section, 'option')
        except:
            Log().logger.warning('option not specified in the ' + self._section +
                                ' section.')

        # build command
        shell_cmd = self._profile.remove_filter(self._section) + " "
        shell_cmd += option
        shell_cmd = os.path.expandvars(shell_cmd)

        # run command
        #Log().logger.info("shell_cmd: " + shell_cmd)
        Log().logger.info('[' + self._section + '] ' + shell_cmd)
        env = Context().env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()

        # handle error
        if proc.returncode != 0:
            Log().logger.error(err.decode(errors='ignore'))
            Log().logger.error(out.decode(errors='ignore'))
            exit(proc.returncode)

        return

    def run(self, in_name):
        # analyze section
        if self._analyze(in_name) < 0:
            return in_name

        # start section
        Log().logger.debug("[" + self._section + "] start section")

        # update predefined environment variable
        base_name = Utils().remove_file_extension(in_name)
        out_name = base_name + '.' + self._profile.remove_filter(self._section)
        Context().add_env_variable('$OF_COMPILE_IN', in_name)
        Context().add_env_variable('$OF_COMPILE_OUT', out_name)
        Context().add_env_variable('$OF_COMPILE_BASE', base_name)

        # add environment variables
        for key in self._profile.options(self._section):
            value = self._profile.get(self._section, key)

            if key.startswith('$'):
                Context().add_env_variable(key, value)

            # elif key.startswith('?'):
            #     self._add_filter(key, value)

            elif key == 'option':
                self._process_option()
                out_name = Context().env().get('OF_COMPILE_OUT')
                if os.path.isfile(out_name) is not True:
                    out_name = in_name

        # set section as completed
        Context().section_completed(self._profile.remove_filter(self._section))

        # end section
        Log().logger.debug("[" + self._section + "] end section")

        return out_name
