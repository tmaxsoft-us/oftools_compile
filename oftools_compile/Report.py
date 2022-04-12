#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to generate the report of the compilation.

Typical usage example:
  report = Report()
  report.add_entry(file_path, rc, elapsed_time)
  report.generate()
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Record(object):
    """A class used to store the result data about each file processing.

    Attributes:
        _count {integer} -- Number of programs being compiled so far.
        _file_name {string} -- Name of the file which has just been processed.
        _working_directory {string} -- Absolute path of the working directory created for the processed file.
        _processing_status {string} -- Status of the processing, either successful or failed.
        _rc {integer} -- Return code of the file processing.
        _last_section {string} -- Name of the last executed section.
        _elapsed_time {integer} -- Elapsed processing time.
    
    Methods:
        __init__(count, file_name, working_directory, processing_status, rc, last_section, elapsed_time) -- Initializes the record with all the attributes.
        to_csv() -- Converts the record data to a CSV record format, with a "," as a delimiter.
    """

    def __init__(self, count, file_name, working_directory, processing_status,
                 rc, last_section, elapsed_time):
        """Initializes the record with all the attributes.
        """
        self._count = count
        self._file_name = file_name
        self._working_directory = working_directory
        self._processing_status = processing_status
        self._rc = rc
        self._last_section = last_section
        self._elapsed_time = elapsed_time

    def to_csv(self):
        """Converts the record data to a CSV record format, with a "," as a delimiter.

        Returns:
             string - A CSV formatted record.
        """
        return str(
            self._count
        ) + ',' + self._file_name + ',' + self._working_directory + ',' + self._processing_status + ',' + str(
            self._rc) + ',' + self._last_section + ',' + str(
                round(self._elapsed_time, 4))


class Report(object):
    """A class used to create a report of the compilation.

    Attributes:
        _success_count {integer} -- Number of successes.
        _fail_count {integer} -- Number of fails.
        _total_time {integer} -- Accumulated elapsed time.

    Methods:
        __init__() -- Initializes the class with all the attributes.
        add_entry(source_file_path, rc, elapsed_time) -- Adds a new record to the report of the compilation.
        summary(clear) -- Generates a quick summary of the compilation.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._success_count = 0
        self._fail_count = 0
        self._total_count = 0
        self._total_time = 0

        self._green = '\x1b[92m'
        self._red = '\x1b[91m'
        self._white = '\x1b[39m'

    def add_entry(self, source_file_path, rc, elapsed_time):
        """Adds a new record to the report of the compilation.

        It first creates the report file if it does not already exist, then analyzes one by one the 
        input parameters, and retrieves some parameters from the Context to create the full report 
        record. Finally, it writes the record to the report file.

        Arguments:
            file_path {string} -- Absolute path of the source file.
            rc {integer} -- Return code of the file processing.
            elapsed_time {integer} --Processing time.

        Raises:
            IndexError: Exception raised if there is no '/' symbol in the filename, which means the file 
                name only has been provided and not the absolute file path.
        """
        if Context().report_file_path == '':
            report_file_name = 'report/oftools_compile' + Context(
            ).tag + Context().time_stamp + '.csv'
            path = os.path.join(Context().root_workdir, report_file_name)
            Log().logger.debug(LogMessage.CREATE_REPORT_FILE.value % path)

            headers = 'count,source,_working_directory,result,rc,section,time(s)'
            Log().logger.debug(LogMessage.WRITE_HEADERS.value % headers)
            FileHandler().write_file(path, headers)
            Context().report_file_path = path

        # Get input source file name
        try:
            source_file_name = source_file_path.rsplit('/', 1)[1]
        except IndexError:
            source_file_name = source_file_path

        # Analyze input parameter: rc
        if rc == 0:
            self._success_count += 1
            build_status = 'SUCCESSFUL'
            color = self._green
        else:
            self._fail_count += 1
            build_status = 'FAILED'
            color = self._red

        Log().logger.info(color + LogMessage.BUILD_STATUS.value %
                          (build_status, round(elapsed_time, 4)) + self._white)
        print('')

        self._total_count = self._success_count + self._fail_count
        record = Record(self._total_count, source_file_name,
                        Context().current_workdir, build_status, rc,
                        Context().last_section, elapsed_time)
        row = record.to_csv()
        FileHandler().write_file(Context().report_file_path, row, mode='a')

        # Analyze input parameter: elapsed_time, cumulate compilation times
        self._total_time += elapsed_time

    def summary(self, clear=False):
        """Generates a quick summary of the compilation.

        If the user enables the clear option, the program deletes the report file and that's why the 
        log message is being skipped.

        Arguments:
            clear {boolean} -- Value of the argument clear from the CLI.
        """
        
        Log().logger.info(LogMessage.REPORT_SUMMARY.value)
        Log().logger.info(LogMessage.TOTAL_PROGRAMS.value % self._total_count)
        Log().logger.info(self._green + LogMessage.TOTAL_SUCCESS.value % self._success_count + self._white)
        Log().logger.info(self._red + LogMessage.TOTAL_FAIL.value % self._fail_count + self._white)
        Log().logger.info(LogMessage.TOTAL_TIME.value %
                          round(self._total_time, 4))

        # Inform the user that the report has been successfully generated
        if clear is False:
            Log().logger.info(LogMessage.REPORT_GENERATED.value %
                              Context().report_file_path)
