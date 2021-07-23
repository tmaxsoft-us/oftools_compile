#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to run the job for any compile section of the profile.

Typical usage example:
  job = CompileJob()
  job.run(file_path_in)
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class CompileJob(Job):
    """A class used to perform all the steps of a compile section.

    Attributes:
        Inherited from Job module.
    
    Methods:
        _analyze(): Analyzes prerequisites before running the job for the section.
        _process_section(): Reads the section line by line to execute the corresponding methods.
        _compile(option): Runs the given shell command with all its options.
        run(file_path_in): Performs all the steps for any compile section of the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates all the following elements:
            - is the section already complete, based on the name without the filter variable
            - is the section mandatory, list of sections in the setup section
            - is the filter of section True or False, if there is one
            - was the the setup section successful

        Returns:
            An integer, the return code of the analysis result.
        """
        if Context().is_section_complete(self._section_name_no_filter):
            rc = 1
        elif Context().is_section_mandatory(self._section_name_no_filter):
            rc = 0
        elif Context().evaluate_filter(self._section_name,
                                       self._filter_name) in (True, None):
            rc = 0
        else:
            rc = 1

        if Context().is_section_complete('setup', skip=False) == False:
            rc = -1
            Log().logger.error(
                '[' + self._section_name +
                '] Cannot proceed: setup section not complete. Aborting compilation job execution'
            )

        return rc

    def _process_section(self):
        """Reads the section line by line to execute the corresponding methods.

        For any compile section, it mainly analyzes the args or 'option' option. And as any other 
        section, it looks for environment and filter variables.

        Returns:
            An integer, the return code of the section execution.
        """
        rc = 0
        Log().logger.debug('[' + self._section_name +
                           '] Starting section, input filename: ' +
                           self._file_path_in)
        Context().last_section = self._section_name

        compilation = False
        status = 'incomplete'

        for key, value in self._profile[self._section_name].items():
            if key == 'args':
                compilation = True
            elif key == 'option':
                if 'args' in self._profile[self._section_name].keys():
                    continue
                else:
                    compilation = True
            else:
                rc = self._process_option(key, value)

            if compilation and status == 'incomplete':
                rc = self._compile(value)
                status = 'done'

            if rc < 0:
                Log().logger.error('[' + self._section_name +
                                   '] Step failed: ' + key +
                                   '. Aborting section execution')
                break

        if rc >= 0:
            Log().logger.debug('[' + self._section_name +
                               '] Ending section, output filename: ' +
                               self._file_name_out)
            Context().section_completed(self._section_name_no_filter)

        return rc

    def _compile(self, option):
        """Runs the given shell command with all its options.

        Returns:
            An integer, the return code of the shell command executed.
        """
        Log().logger.debug('[' + self._section_name +
                           '] Processing compilation')

        # Build command
        shell_command = self._section_name_no_filter + ' ' + option

        # Run command
        Log().logger.info('[' + self._section_name + '] ' +
                          os.path.expandvars(shell_command))
        _, _, rc = Utils().execute_shell_command(shell_command, 'compile',
                                                 Context().env)

        return rc

    def run(self, file_path_in):
        """Performs all the steps for any compile section of the profile.

        Returns:
            An integer, the return code of the given compile section.
        """
        self._initialize_file_variables(file_path_in)
        self._update_context()

        rc = self._analyze()
        if rc != 0:
            if rc > 0:
                rc = 0
            self._file_name_out = file_path_in
            return rc

        rc = self._process_section()
        if rc != 0:
            self._file_name_out = file_path_in
            return rc

        return rc
