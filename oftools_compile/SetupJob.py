#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to run the job for the setup section of the profile.

Typical usage example:
  job = SetupJob()
  job.run(file_path_in)
"""

# Generic/Built-in modules
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log


class SetupJob(Job):
    """A class used to perform all the steps of a setup section.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze(): Analyzes prerequisites before running the job for the section.
        _process_section(): Reads the section line by line to execute the corresponding methods.
        _init_current_workdir(): Initializes the working directory for the file being currently 
            processed.
        _init_file(): Copies the file to the working directory.
        _init_log_file(): Initializes the log file for the file being currently processed.
        run(file_path_in): Performs all the steps for the setup section of the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates the following statements:
            - is the section already complete, based on the name without the filter variable
            - is the section mandatory, list of sections in the setup section
            - is the filter of section True or False, if there is one

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

        return rc

    def _process_section(self):
        """Reads the section line by line to execute the corresponding methods.

        For the setup section, it mainly analyzes the workdir and mandatory options. And as any other 
        section, it looks for environment and filter variables.

        Returns:
            An integer, the return code of the section execution. 
        """
        rc = 0
        Log().logger.debug('[' + self._section_name +
                           '] Starting section, input filename: ' +
                           self._file_path_in)
        Context().last_section = self._section_name

        for key, value in self._profile[self._section_name].items():
            if key == 'workdir':
                self._init_current_workdir()
                rc = self._init_file()
                self._init_log_file()
            elif key == 'mandatory':
                continue
            elif key == 'housekeeping':
                #TODO Code housekeeping feature
                continue
            else:
                rc = self._process_option(key, value)

            if rc != 0:
                Log().logger.error('[' + self._section_name +
                                   '] Step failed: ' + key +
                                   '. Aborting section execution')
                break

        if rc == 0:
            Log().logger.debug('[' + self._section_name +
                               '] Ending section, output filename: ' +
                               self._file_name_out)
            Context().section_completed(self._section_name_no_filter)

        return rc

    def _init_current_workdir(self):
        """Initializes the working directory for the file being currently processed.
        """
        Log().logger.debug('[' + self._section_name +
                           '] Creating working directory')

        while True:
            current_workdir = os.path.join(
                Context().root_workdir,
                self._file_name_in + Context().tag + Context().time_stamp)

            # Check if the working directory already exists
            if not os.path.isdir(current_workdir):
                os.mkdir(current_workdir)
                break
            else:
                Log().logger.warning(
                    '[' + self._section_name +
                    '] Working directory already exists: ' + current_workdir +
                    '. Sleeping 1 second to assign a new time stamp')
                Context().time_stamp = 1

        # Change directory to current working directory and update Context
        os.chdir(current_workdir)
        Context().current_workdir = current_workdir

    def _init_file(self):
        """Copies the file to the current working directory.

        Returns:
            An integer, the return code of the copy of the file.
        """
        current_workdir = Context().current_workdir
        Log().logger.debug('[' + self._section_name + '] Processing file copy')

        try:
            shutil.copy(self._file_path_in, current_workdir)
            rc = 0
        except shutil.SameFileError as e:
            rc = -1
            Log().logger.error('[' + self._section_name +
                               '] Failed to copy: %s' % e)
        except OSError as e:
            rc = -1
            Log().logger.error('[' + self._section_name +
                               '] Failed to copy: %s' % e)
        finally:
            return rc

    def _init_log_file(self):
        """Initializes the log file for the file being currently processed.

        It first opens the file, then write the header and the setup section steps to the file.
        """
        current_workdir = Context().current_workdir
        Log().logger.debug('[' + self._section_name + '] Creating log file')
        Log().open_file(os.path.join(current_workdir, 'oftools_compile.log'))

        header = '================================================================================'
        header = header[0:4] + ' ' + self._file_name_in + ' ' + header[
            len(self._file_name_in) + 4:]

        Log().logger.info(header)
        Log().logger.info('[' + self._section_name + '] mkdir ' +
                          current_workdir)
        Log().logger.info('[' + self._section_name + '] cd ' + current_workdir)
        Log().logger.info('[' + self._section_name + '] cp ' +
                          self._file_path_in + ' ' + current_workdir)

    def run(self, file_path_in):
        """Performs all the steps for the setup section of the profile.

        Returns:
            An integer, the return code of the setup section.
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
