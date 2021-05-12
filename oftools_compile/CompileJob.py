#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
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
    """

    Attributes:
        Inherited from Job module.
    
    Methods:
        _analyze():
        _process_section():
        _process_option(option):
        run(file_path_in):
    """

    def _analyze(self):
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
            rc = -1
        else:
            rc = 0

        return rc

    def _process_section(self):
        """
        """
        Log().logger.debug('[' + self._section_name +
                           '] start section. Processing options')

        for key, value in self._profile[self._section_name].items():
            if key == 'option':
                self._process_option(value)
                #? Potential issue with file name here?
                file_name_out = Context().env['OF_COMPILE_OUT']
                if os.path.isfile(file_name_out) == False:
                    self._file_name_out = self._file_name_in
            else:
                self._process_option(key, value)

    def _process_option(self, option):
        """
        """
        # Build command
        shell_command = self._section_name_no_filter + ' ' + option

        # Run command
        Log().logger.info('[' + self._section_name + '] ' + shell_command)
        out, err, rc = Utils().execute_shell_command(shell_command, Context().env)

        # Handle error
        if rc != 0:
            Log().logger.error(err.decode(errors='ignore'))
            Log().logger.error(out.decode(errors='ignore'))
            exit(rc)

        return

    def run(self, file_path_in):
        """
        """
        if self._analyze() < 0:
            return file_path_in

        # Detect if the source provided is a file or a directory, and properly retrieve the name of the file
        self._initialize_file_variables(file_path_in)
        # Update Context with name of files being manipulated in this job execution
        self._update_context()
        # Analysis of the compile section
        self._process_section()

        # TODO Put a condition to make sure that the section has been properly completed
        # Clear file variables, set compile section as completed and write end section to log file
        self._clear()

        return self._file_name_out
