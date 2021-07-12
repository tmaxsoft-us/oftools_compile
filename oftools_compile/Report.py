#!/usr/bin/python3
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
from .Log import Log


class Record(object):
    """A class used to store the result data about each file processing.

    Attributes:
        _count: An integer, the number of programs being compiled so far.
        _file_name: A string, the name of the file which has been processed.
        _current_workdir: A string, the path of the working directory created for the processed file.
        _processing_status: A string, whether the processing has been successful or failed.
        _rc: An integer, the return code of the file processing.
        _last_section: A string, the name of the last executed section.
        _elapsed_time: An integer, for a given program this is the elapsed processing time.
    
    Methods:
        __init__(count, file_name, current_workdir, processing_status, rc, last_section, elapsed_time): 
            Initializes the record with all the attributes.
        to_csv(): Convert the record data to a CSV record format, with a space as a delimiter.
    """

    def __init__(self, count, file_name, current_workdir, processing_status, rc,
                 last_section, elapsed_time):
        """Initializes the record with all the attributes.
        """
        self._count = count
        self._file_name = file_name
        self._current_workdir = current_workdir
        self._processing_status = processing_status
        self._rc = rc
        self._last_section = last_section
        self._elapsed_time = elapsed_time

    def to_csv(self):
        """Convert the record data to a CSV record format, with a space as a delimiter.

        Returns:
            A string, the record with a CSV format.
        """
        return str(
            self._count
        ) + ',' + self._file_name + ',' + self._current_workdir + ',' + self._processing_status + ',' + str(
            self._rc) + ',' + self._last_section + ',' + str(
                round(self._elapsed_time, 4))


class Report(object):
    """A class used to create a report of the compilation.

    Attributes:
        _success_count: An integer, the number of successes.
        _fail_count: An integer, the number of fails.
        _total_time: An integer, the accumulated elapsed time.

    Methods:
        __init__(): Initializes the class with all the attributes.
        add_entry(file_path, rc, elapsed_time): Adds a new record to the report of the compilation.
        summary(clear): Generates a quick summary of the compilation.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._success_count = 0
        self._fail_count = 0
        self._total_time = 0

    def add_entry(self, source_file_path, rc, elapsed_time):
        """Adds a new record to the report of the compilation.

        It first creates the report file if it does not already exist, then analyzes one by one the 
        input parameters, and retrieves some parameters from the Context to create the full report 
        record. Finally, it writes the record to the report file.

        Args:
            file_path: A string, the absolute path of the source file.
            rc: An integer, the return code of the file processing.
            elapsed_time: An integer, the processing time.

        Raises:
            IndexError: An error occurs if there is no '/' symbol in the filename, which means the file 
                name only has been provided and not the absolute file path.
        """
        # Create report file
        if Context().report_file_path == '':
            report_file_name = 'report/oftools_compile' + Context(
            ).tag + Context().time_stamp + '.csv'
            Context().report_file_path = os.path.expandvars(
                os.path.join(Context().root_workdir, report_file_name))
            # Writing headers to the report file
            with open(Context().report_file_path, 'w') as fd:
                fd.write('count,source,list_dir,result,rc,section,time(s)\n')
                #fd.write('COUNT SOURCE LIST_DIR RESULT RC SECTION TIME(s)\n')
                #fd.write('----- ---------- -------------------- -------- -- --------- -------\n')

        # Analyze input parameter: file_path
        try:
            source_file_name = source_file_path.rsplit('/', 1)[1]
        except IndexError:
            source_file_name = source_file_path

        # Analyze input parameter: rc
        if rc >= 0:
            self._success_count += 1
            processing_status = 'SUCCESS'
        else:
            self._fail_count += 1
            processing_status = 'FAILED'
        Log().logger.info('BUILD ' + processing_status + ' (' +
                          str(round(elapsed_time, 4)) + ' s)')
        print('')

        # Analyze input parameter: elapsed_time, cumulate compilation times
        self._total_time += elapsed_time

        count = self._success_count + self._fail_count
        record = Record(count, source_file_name,
                        Context().current_workdir, processing_status, rc,
                        Context().last_section, elapsed_time)

        with open(Context().report_file_path, 'a') as fd:
            line = record.to_csv()
            fd.write('%s\n' % line)

    def summary(self, clear=False):
        """Generates a quick summary of the compilation.

        If the user enables the clear option, the program deletes the report file and that's why the 
        log message is being skipped.

        Args:
            clear: A boolean, the value of the argument clear from the CLI.
        """
        Log().logger.info(
            '===== SUMMARY =================================================================='
        )
        Log().logger.info('TOTAL     : ' +
                          str(self._success_count + self._fail_count))
        Log().logger.info('SUCCESS   : ' + str(self._success_count))
        Log().logger.info('FAILED    : ' + str(self._fail_count))
        Log().logger.info('TOTAL TIME: ' + str(round(self._total_time, 4)) +
                          ' sec')

        # Inform the user that the report has been successfully generated
        if clear is False:
            Log().logger.info('REPORT: CSV report successfully generated: ' +
                              Context().report_file_path)
