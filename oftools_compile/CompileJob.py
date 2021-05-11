#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import subprocess

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class CompileJob(Job):
    """

    Attributes:
        Inherited from Job module.
    
    Methods:
        _process_section():
        _process_option():
        run(file_path_in):
    """

    def _process_option(self):
        """
        """
        Log().logger.debug('[' + self._section_name +
                           '] start section. Processing options')
        option = ""

        try:
            option = self._profile.get(self._section_name, 'option')
        except:
            Log().logger.warning('option not specified in the ' +
                                 self._section_name + ' section.')

        # build command
        shell_cmd = self._profile.remove_filter(self._section_name) + " "
        shell_cmd += option
        shell_cmd = os.path.expandvars(shell_cmd)

        # run command
        #Log().logger.info("shell_cmd: " + shell_cmd)
        Log().logger.info('[' + self._section_name + '] ' + shell_cmd)
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

    def run(self, file_path_in):
        """
        """
        # Check if setup section was successful
        if Context().is_section_complete('setup') == False:
            Log().logger.error(
                'cannot proceed due to setup not being completed.')
            #? We really need to exit here?
            exit(-1)
        # Analyze prerequisites before running the job for the section
        # Include completion of section and filter evaluation if there is one
        if self._is_section_complete() < 0 or self._filter_evaluation(
        ) == False:
            return file_path_in

        # update predefined environment variable
        base_name = Utils().remove_file_extension(file_path_in)
        out_name = base_name + '.' + self._profile.remove_filter(
            self._section_name)
        Context().add_env_variable('$OF_COMPILE_IN', file_path_in)
        Context().add_env_variable('$OF_COMPILE_OUT', out_name)
        Context().add_env_variable('$OF_COMPILE_BASE', base_name)

        # add environment variables
        for key in self._profile.options(self._section_name):
            value = self._profile.get(self._section_name, key)

            if key.startswith('$'):
                Context().add_env_variable(key, value)

            # elif key.startswith('?'):
            #     self._add_filter(key, value)

            elif key == 'option':
                self._process_option()
                out_name = Context().env().get('OF_COMPILE_OUT')
                if os.path.isfile(out_name) is not True:
                    out_name = file_path_in

        # set section as completed
        Context().section_completed(self._section_name_no_filter)

        # end section
        Log().logger.debug("[" + self._section_name + "] end section")

        return out_name
