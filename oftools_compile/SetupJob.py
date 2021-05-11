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
        _init_current_workdir():
        _init_log_file(current_workdir):
        run(file_path_in):
    """

    def _analyze(self):
        """
        """
        # Check if given section is already completed
        if Context().is_section_complete(self._section_name):
            return -1

        return 0

    def _process_section(self):
        """
        """
        Log().logger.debug('[' + self._section_name + '] process options')

        for key, value in self._profile[self._section_name].items():
            if key == 'workdir':
                current_workdir = self._init_current_workdir()
                self._init_log_file(current_workdir)
            else:
                self._analyze_common_options(key, value)

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
        #? Is it still useful?
        # Analyze prerequisites before running the job for the section
        if self._analyze() < 0:
            Log().logger.debug('[' + self._section_name + '] skip section')
            return file_path_in

        if self._filter_name != '':
            Context().evaluate_filter(self._filter_name)
            if Context().filter_results(self._filter_name) == False:
                Log().logger.debug(
                    '[' + self._section_name +
                    '] Result of filter variable evaluation: False. Skipping section.')
                return file_path_in

        # Detect if the source provided is a file or a directory, and properly retrieve the name of the file
        self._initialize_file_variables(file_path_in)
        # Update Context with name of files being manipulated in this job execution
        self._update_context()
        # Analysis of the setup section
        self._process_section()

        #? Same question as always, what is it for?
        # Set the mandatory section
        sections = self._profile.sections()
        if 'deploy' in sections:
            for section in reversed(sections):
                if section.startswith('deploy') is False:
                    Log().logger.debug('[' + self._section_name +
                                       '] mandatory section: ' + section)
                    Context().mandatory_section(section)
                    break

        # set section as completed
        Context().section_completed(self._section_no_filter)

        self._clear()

        return self._file_name_out
