#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run the job for any profile compile section.

Typical usage example:
  job = CompileJob()
  job.run(file_path_in)
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from ..Context import Context
from ..enums.LogEnum import LogMessage
from ..handlers.ShellHandler import ShellHandler
from .Job import Job
from ..Log import Log


class CompileJob(Job):
    """A class used to perform all the steps of a compile section.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze() -- Analyzes prerequisites before running the job for the
            section.
        _process_section() -- Reads the section line by line to execute the
            corresponding methods.
        _compile(args) -- Runs the given shell command with all its arguments.
        run(file_path_in) -- Performs all the steps for any compile section of
            the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates all the following elements:
            - is the section already complete, based on the name without the
                filter function
            - is the section mandatory, list of sections in the setup section
            - is the filter of the section True or False, if there is one
            - is the the setup section successful or not

        Returns:
            integer -- Return code of the analysis.
        """
        filter_function = Context().get_filter_function(self._filter)

        if self._profile.is_section_complete(self._section_name):
            return_code = 1
        elif self._profile.is_section_mandatory(self._section_name):
            return_code = 0
        elif ShellHandler().evaluate_filter(filter_function, self._filter,
                                            self._section_name,
                                            Context().env) in (True, None):
            return_code = 0
        else:
            return_code = 1

        return return_code

    def _process_section(self):
        """Reads the section line by line to execute the corresponding methods.

        For any compile section, it mainly analyzes the args or "option"
        option. And as any other section, it looks for environment and filter
        variables.

        Returns:
            integer -- Return code of the method.
        """
        return_code = 0
        Log().logger.debug(LogMessage.START_SECTION.value %
                           (self._section_name, self._file_path_in))

        compilation = False
        status = "incomplete"

        for key, value in self._profile.data[self._section_name].items():
            if key == "args":
                compilation = True
            elif key == "option":
                if "args" in self._profile.data[self._section_name].keys():
                    continue
                else:
                    compilation = True
            else:
                return_code = self._process_option(key, value)

            if compilation and status == "incomplete":
                return_code = self._compile(value)
                status = "done"

            if return_code not in (0, 1):
                Log().logger.error(LogMessage.ABORT_SECTION.value %
                                   (self._section_name, key))
                break

        if return_code in (0, 1):
            Log().logger.debug(LogMessage.END_SECTION.value %
                               (self._section_name, self._file_name_out))
            self._profile.section_completed(self._section_no_filter)

        return return_code

    def _compile(self, args):
        """Runs the given shell command with all its arguments.

        Arguments:
            args {string} -- Arguments of the command being executed.

        Returns:
            integer -- Return code of the shell command executed.
        """
        # Build command
        shell_command = self._section_no_filter + " " + args

        # Run command
        Log().logger.info(
            LogMessage.RUN_COMMAND.value %
            (self._section_name, os.path.expandvars(shell_command)))
        _, _, return_code = ShellHandler().execute_command(shell_command,
                                                  env=Context().env)

        return return_code

    def run(self, file_path_in):
        """Performs all the steps for any compile section of the profile.

        Returns:
            integer -- Return code of the given compile section.
        """
        self._initialize_file_variables(file_path_in)
        self._update_context()

        return_code = self._analyze()
        if return_code != 0:
            self._file_name_out = file_path_in
            return return_code

        return_code = self._process_section()
        if return_code not in (0, 1):
            self._file_name_out = file_path_in

        return return_code
