#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os
import shutil
import time

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log


class SetupJob(Job):
    """

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze():
        _process_section():
        _init_current_workdir():
        _init_log_file(current_workdir):
        run(file_path_in):
    """

    def _analyze(self):
        """
        """
        #? Is section completed still useful?
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
            if key == 'workdir':
                current_workdir = self._init_current_workdir()
                self._init_log_file(current_workdir)
            else:
                self._process_option(key, value)

    def _init_current_workdir(self):
        """
        """
        current_workdir = os.path.join(
            Context().root_workdir,
            self._file_name_in + Context().tag + Context().time_stamp)

        while True:
            if not os.path.isdir(current_workdir):
                os.mkdir(current_workdir)
                break

            Log().logger.warning(
                current_workdir +
                ' already exists. Sleeping 1 second to assign a new time stamp.'
            )
            time.sleep(1)
            current_workdir = os.path.join(
                Context().root_workdir,
                self._file_name_in + Context().tag + Context().time_stamp)

        # Copy source file to the current work directory
        shutil.copy(self._file_path_in, current_workdir)
        # Change directory to work directory
        os.chdir(current_workdir)
        # Update Context with the current work directory
        Context().current_workdir(current_workdir)

        return current_workdir

    def _init_log_file(self, current_workdir):
        """
        """
        Log().open_file(os.path.join(current_workdir, 'oftools_compile.log'))

        header = '============================================================'
        header = header[:1] + ' ' + self._file_name_in + ' ' + header[
            len(self._file_name_in) + 2:]

        Log().logger.info(header)
        Log().logger.info('[' + self._section_name + '] ' + 'mkdir ' +
                          current_workdir)
        Log().logger.info('[' + self._section_name + '] ' + 'cp ' +
                          self._file_path_in + ' ' + current_workdir)
        Log().logger.info('[' + self._section_name + '] ' + 'cd ' +
                          current_workdir)

    def run(self, file_path_in):
        """
        """
        if self._analyze() < 0:
            return file_path_in

        # Detect if the source provided is a file or a directory, and properly retrieve the name of the file
        self._initialize_file_variables(file_path_in)
        # Update Context with name of files being manipulated in this job execution
        self._update_context()
        # Analysis of the setup section
        self._process_section()

        #? Same question as always, what is mandatory section for?
        # Set the mandatory section
        sections = self._profile.sections()
        if 'deploy' in sections:
            for section in reversed(sections):
                if section.startswith('deploy') is False:
                    Log().logger.debug('[' + self._section_name +
                                       '] mandatory section: ' + section)
                    Context().mandatory_section(section)
                    break

        # TODO Put a condition to make sure that the section has been properly completed
        # Clear file variables, set setup section as completed and write end section to log file
        self._clear()

        return self._file_name_out
