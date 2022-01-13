#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run the job for the setup section of the profile.

Typical usage example:
  job = SetupJob()
  job.run(file_path_in)
"""

# Generic/Built-in modules
import datetime
import os
import shutil

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .FileHandler import FileHandler


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
            - is the section already complete, based on the name without the filter function
            - is the section mandatory, list of sections in the setup section
            - is the filter of the section True or False, if there is one

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
            elif key == 'backup' and self._profile.has_option(
                    'setup', 'housekeeping') is False:
                rc = self._process_backup(value)
            elif key == 'housekeeping':
                rc = self._process_housekeeping(value)
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

    def _process_backup(self, value):
        """Clean the root working directory from old compilation directories based on the number of backups.

            Arguments:
                value {string} -- The value of the backup option, this is an integer.

            Returns:
                integer -- The return code of the method.

            Raises:
                ValueError: An error occurs if the input value cannot be converted from string to integer.
            """
        try:
            value = int(value)
            backup_paths = FileHandler().get_duplicates(
                Context().root_workdir,
                self._file_name_in,
            )[1]

            if len(backup_paths) > value:
                creation_times = FileHandler().get_creation_times(backup_paths)

                # Sorting the backup_paths list based on a sorting of the creation_times list
                backup_paths = [
                    path
                    for _, path in sorted(zip(creation_times, backup_paths))
                ]

                while len(backup_paths) > value:
                    backup = backup_paths[0]
                    backup_paths.pop(0)

                    #Deletion of the directory
                    FileHandler().delete_directory(backup)
            rc = 0

            Log().logger.error(
                '[setup] Invalid value for the "backup" option: It must be an integer'
            )
            rc = -1
        except ValueError:
            Log().logger.error(
                '[setup] ValueError: The "backup" option must be an integer')
            rc = -1

        return rc

    def _process_housekeeping(self, value):
        """Clean the root working directory from compilation directories older than the input date.

            Arguments:
                value {string} -- The value of the housekeeping option, this is a number of days.

            Returns:
                integer -- The return code of the method.

            Raises:
                ValueError: An error occurs if part of the input value cannot be converted from string to integer.
            """
        try:
            days = int(value[:-1])
            if value[-1] == 'd' and isinstance(value[:-1], int):
                if self._profile.has_option('setup', 'backup'):

                    backup_value = self._profile.get('setup', 'backup')
                    threshold = datetime.datetime.today() - datetime.timedelta(
                        days=int(days))

                    backup_paths = FileHandler().get_duplicate_directories(
                        Context().root_workdir, self._file_name_in,
                        'directories')

                    if len(backup_paths) > backup_value:
                        creation_times = FileHandler().get_creation_times(
                            backup_paths)

                        # Sorting the creation_times list
                        creation_times_sorted = creation_times.sort()
                        # Sorting the backup_paths list based on a sorting on the creation_times list
                        backup_paths = [
                            path for _, path in sorted(
                                zip(creation_times, backup_paths))
                        ]

                        number_of_backups = len(backup_paths)
                        for i in range(len(backup_paths)):
                            backup_creation_date = datetime.datetime.fromtimestamp(
                                creation_times_sorted[i])

                            if backup_creation_date < threshold:
                                backup = backup_paths[i]
                                number_of_backups -= 1

                                #Deletion of the directory
                                FileHandler().delete_directory(backup)

                            if number_of_backups == backup_value:
                                break
                    rc = 0

                else:
                    Log().logger.warning(
                        '[setup] "backup" value required to run housekeeping')
                    rc = 1
        except ValueError:
            Log().logger.error(
                '[setup] ValueError: The "housekeeping" option must be a number of days, for example: 30d'
            )
            rc = -1

        return rc

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
