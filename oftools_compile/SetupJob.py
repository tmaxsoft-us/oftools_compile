#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run the job for the profile setup section.

Typical usage example:
  job = SetupJob()
  job.run(file_path_in)
"""

# Generic/Built-in modules
import datetime
import os

# Third-party modules

# Owned modules
from .Context import Context
from .enums.ErrorEnum import ErrorMessage
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .handlers.ShellHandler import ShellHandler
from .Job import Job
from .Log import Log


class SetupJob(Job):
    """A class used to perform all the setup section steps.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze() -- Analyzes prerequisites before running the job for the section.
        _process_section() -- Reads the section line by line to execute the corresponding methods.
        _init_current_workdir() -- Initializes the working directory for the file being currently 
            processed.
        _init_file() -- Copies the file to the working directory.
        _init_log_file() -- Initializes the log file for the file being currently processed.
        _process_backup(value) -- Cleans the root working directory from old compilation directories based on the number of backups to be kept.
        _process_housekeeping(value) -- Cleans the root working directory from compilation directories older than the input number of days.
        run(file_path_in) -- Performs all the steps for the setup section of the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates the following statements:
            - is the section already complete, based on the name without the filter function
            - is the section mandatory, list of sections in the setup section
            - is the filter of the section True or False, if there is one

        Returns:
            integer - Return code of the analysis.
        """
        filter_function = Context().get_filter_function(self._filter)

        if Context().is_section_complete(self._section_name,
                                         self._section_no_filter):
            rc = 1
        elif Context().is_section_mandatory(self._section_name,
                                            self._section_no_filter):
            rc = 0
        elif ShellHandler().evaluate_filter(filter_function, self._filter,
                                            self._section_name,
                                            Context().env) in (True, None):
            rc = 0
        else:
            rc = 1

        return rc

    def _process_section(self):
        """Reads the section line by line to execute the corresponding methods.

        For the setup section, it mainly analyzes the workdir options, but also processes options such as mandatory, backup and housekeeping. And as any other 
        section, it looks for environment and filter variables.

        Returns:
            integer -- Return code of the method.
        """
        rc = 0
        Log().logger.debug(LogMessage.START_SECTION.value %
                           (self._section_name, self._file_path_in))

        for key, value in self._profile[self._section_name].items():
            if key == 'workdir':
                rc = self._init_current_workdir()
                if rc != 0:
                    Log().logger.error(LogMessage.ABORT_SECTION.value %
                                       (self._section_name, key))
                    break
                rc = self._init_file()
                self._init_log_file()
            elif key == 'mandatory':
                continue
            elif key == 'backup' and self._profile.has_option(
                    'setup', 'housekeeping') is False:
                rc = self._process_backup(value)
            elif key == 'housekeeping':
                rc = self._process_housekeeping(value)
            else:
                rc = self._process_option(key, value)

            if rc != 0:
                Log().logger.error(LogMessage.ABORT_SECTION.value %
                                   (self._section_name, key))
                break

        if rc == 0:
            Log().logger.debug(LogMessage.END_SECTION.value %
                               (self._section_name, self._file_name_out))
            Context().section_completed(self._section_no_filter)

        return rc

    def _init_current_workdir(self):
        """Initializes the working directory for the file being currently processed.

        Returns:
            integer -- Return code of the method.
        """
        Log().logger.debug(LogMessage.START_WORKING_DIRECTORY.value %
                           self._section_name)

        while True:
            current_workdir = os.path.join(
                Context().root_workdir,
                self._file_name_in + Context().tag + Context().time_stamp)

            rc = FileHandler().create_directory(current_workdir)
            if rc != 0:
                Log().logger.debug(LogMessage.ADD_TIME_TO_TIME_STAMP.value %
                                   (self._section_name, current_workdir))
                Context().time_stamp = 1
            else:
                # Update Context and change directory to current working directory
                Context().current_workdir = current_workdir
                os.chdir(current_workdir)
                break

        Log().logger.debug(LogMessage.END_WORKING_DIRECTORY.value %
                           self._section_name)

        return rc

    def _init_file(self):
        """Copies the file to the current working directory.

        Returns:
            integer -- Return code of the method.
        """
        Log().logger.debug(LogMessage.START_SETUP_FILE.value %
                           self._section_name)

        current_workdir = Context().current_workdir
        rc = FileHandler().copy_file(self._file_path_in, current_workdir)

        Log().logger.debug(LogMessage.END_SETUP_FILE.value % self._section_name)

        return rc

    def _init_log_file(self):
        """Initializes the log file for the file being currently processed.

        It first opens the file, then write the header and the setup section steps to the file.
        """
        Log().logger.debug(LogMessage.START_LOG_FILE.value % self._section_name)

        current_workdir = Context().current_workdir
        Log().open_file(os.path.join(current_workdir, 'oftools_compile.log'))
        header = '================================================================================'
        header = header[0:4] + ' ' + self._file_name_in + ' ' + header[
            len(self._file_name_in) + 4:]

        Log().logger.info(header)
        Log().logger.info(LogMessage.MKDIR_COMMAND.value %
                          (self._section_name, current_workdir))
        Log().logger.info(LogMessage.CD_COMMAND.value %
                          (self._section_name, current_workdir))
        Log().logger.info(
            LogMessage.CP_COMMAND.value %
            (self._section_name, self._file_path_in, current_workdir))

        Log().logger.debug(LogMessage.END_LOG_FILE.value % self._section_name)

    def _process_backup(self, value):
        """Cleans the root working directory from old compilation directories based on the number of backups to be kept.

        Arguments:
            value {string} -- Value of the backup option, this is an integer.

        Returns:
            integer -- Return code of the method.

        Raises:
            ValueError -- Exception raised if the input value cannot be converted from string to integer.
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
        except ValueError:
            Log().logger.error(ErrorMessage.VALUE_BACKUP.value)
            rc = -1

        return rc

    def _process_housekeeping(self, value):
        """Cleans the root working directory from compilation directories older than the input number of days.

        Arguments:
            value {string} -- Value of the housekeeping option, this must be a number of days.

        Returns:
            integer -- Return code of the method.

        Raises:
            ValueError -- Exception raised if part of the input value cannot be converted from string to integer.
        """
        try:
            if self._profile.has_option('setup', 'backup'):
                #TODO Improve the two lines below
                days = int(value[:-1])
                if value[-1] == 'd' and isinstance(value[:-1], int):

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
            Log().logger.error(ErrorMessage.VALUE_HOUSEKEEPING.value)
            rc = -1

        return rc

    def run(self, file_path_in):
        """Performs all the steps for the setup section of the profile.

        Returns:
            integer -- Return code of the setup section.
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
