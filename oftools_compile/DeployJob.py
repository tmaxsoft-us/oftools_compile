#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""
# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class DeployJob(Job):
    """

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze():
        _process_file():
        _process_section():
        _process_dataset(option):
        _process_region(option):
        _process_tdl(option):
        run(file_path_in):
    """

    def _analyze(self):
        """
        """
        # Check if any compile job was successful
        if Context().is_mandatory_section_complete() is False:
            Log().logger.error(
                'mandatory section [' + Context().mandatory_section() +
                '] did not ran successfully. aborting the deploy job')
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

    def _process_file(self):
        """
        """
        try:
            self._file_name_out = self._profile('deploy', 'file')
            self._file_name_out = os.path.expandvars(self._file_name_out)

            if self._file_name_in != self._file_name_out:
                Log().logger.info('[' + self._section_name + '] ' + 'cp ' +
                                  self._file_name_in + ' ' +
                                  self._file_name_out)
                shutil.copy(self._file_name_in, self._file_name_out)
        #TODO What type of exception is raised here?
        except:
            Log().logger.error('[' + self._section_name + '] failed to copy ' +
                               self._file_name_in)
            exit(-1)

    def _process_section(self):
        """
        """
        Log().logger.debug('[' + self._section_name +
                           '] start section. Processing options')

        for key, value in self._profile[self._section_name].items():
            if key == 'dataset':
                self._process_dataset(value)
            elif key == 'region':
                self._process_region(value)
            elif key == 'tdl':
                self._process_tdl(value)
            else:
                self._process_option(key, value)

    def _process_dataset(self, option):
        """
        """
        datasets = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for dataset in datasets:
            shell_command = 'dlupdate ' + file_path_out + ' ' + dataset
            Log().logger.info('[' + self._section_name + '] ' + shell_command)
            out, err, rc = Utils().execute_shell_command(
                shell_command,
                Context().env)

            # Handle result
            if rc != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(rc)

    def _process_region(self, option):
        """
        """
        regions = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for region in regions:
            region_path = os.path.join('$OPENFRAME_HOME/osc/region',
                                       os.path.expandvars(region) + '/tdl/mod')
            shell_command = 'cp ' + file_path_out + ' ' + region_path
            Log().logger.info('[' + self._section_name + '] ' + shell_command)
            out, err, rc = Utils().execute_shell_command(
                shell_command,
                Context().env)
            # Handle result
            if rc != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(rc)

            shell_command = 'osctdlupdate ' + region + ' ' + self._file_name_out
            Log().logger.info('[' + self._section_name + '] ' + shell_command)
            out, err, rc = Utils().execute_shell_command(
                shell_command,
                Context().env)
            # Handle result
            if rc != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(rc)

    def _process_tdl(self, option):
        """
        """
        tdls = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for tdl in tdls:
            tdl_path = os.path.join(os.path.expandvars(tdl) + '/tdl/mod')
            shell_command = 'cp ' + file_path_out + ' ' + tdl_path
            Log().logger.info('[' + self._section_name + '] ' + shell_command)
            out, err, rc = Utils().execute_shell_command(
                shell_command,
                Context().env)
            # Handle result
            if rc != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(rc)

            shell_command = 'tdlupdate -m ' + file_path_out + ' -r ' + tdl_path
            Log().logger.info('[' + self._section_name + '] ' + shell_command)
            out, err, rc = Utils().execute_shell_command(
                shell_command,
                Context().env)
            # Handle result
            if rc != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(rc)

    def run(self, file_path_in):
        """
        """
        if self._analyze() < 0:
            return file_path_in

        # Detect if the source provided is a file or a directory, and properly retrieve the name of the file
        self._initialize_file_variables(file_path_in)
        # Update Context with name of files being manipulated in this job execution
        self._update_context()
        # Change output file name depending on the option file in the profile, and then copy the file
        self._process_file()

        # Analysis of the compile section
        self._process_section()

        #TODO Put a condition to make sure that the section has been properly completed
        # Clear file variables, set compile section as completed and write end section to log file
        self._clear()

        return self._file_name_out
