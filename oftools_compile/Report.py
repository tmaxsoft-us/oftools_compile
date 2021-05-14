#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log


class Record(object):
    _rc = 0
    _source = ""
    _section = ""
    _unit_time = 0

    def __init__(self, source_file, list_dir, last_section, compilation_status,
                 elapsed_time):
        self._source_file = source_file
        self._list_dir = list_dir
        self._last_section = last_section
        self._compilation_status = compilation_status
        self._elapsed_time = elapsed_time

    def to_csv(self):
        return str(self._source_file + ',' + self._list_dir + ',' +
                   self._last_section + ',' + self._compilation_status + ',' +
                   str(round(self._elapsed_time, 4)))


class Report(object):
    """

    Attributes:
        _success_count:
        _fail_count:
        _total_time:

    Methods:
        __init__():
        add_entry():
        generate():
    """

    def __init__(self):
        """
        """
        self._success_count = 0
        self._fail_count = 0
        self._total_time = 0

        self._records = []

    def add_entry(self, source_file, last_job, return_code, elapsed_time):
        """
        """
        # Is the compilation a success or a failure?
        if return_code >= 0:
            compilation_status = 'S'
            self._success_count += 1
            Log().logger.info('BUILD SUCCESS (' + str(round(elapsed_time, 4)) +
                              ' sec)')
        else:
            compilation_status = 'F'
            self._fail_count += 1
            Log().logger.info('BUILD FAILED (' + str(round(elapsed_time, 4)) +
                              ' sec)')
        Log().logger.info('')

        # Cumulate compilation times
        self._total_time += elapsed_time

        # Retrieve section corresponding to the latest job for the report
        #? Do we really want to remove the filter here? The user doesn't want to know exactly the section executed?
        last_section = last_job._remove_filter_name(last_job.section)

        #? Still mandatory section?????????
        if last_section.startswith('deploy'):
            if Context().is_mandatory_section_complete() is False:
                last_section = Context().mandatory_section

        #? Record class useless for me, only elapsed time need to be cast to string
        record = Record(source_file,
                        Context().current_workdir, last_section,
                        compilation_status, elapsed_time)
        self._records.append(record)

    def generate(self):
        """
        """
        # Write summary to log
        Log().logger.info(
            '= SUMMARY ==================================================')
        Log().logger.info('TOTAL     : ' +
                          str(self._success_count + self._fail_count))
        Log().logger.info('SUCCESS   : ' + str(self._success_count))
        Log().logger.info('FAILED    : ' + str(self._fail_count))
        Log().logger.info('TOTAL TIME: ' + str(round(self._total_time, 4)) +
                          ' sec')

        # Create report file
        report_name = 'report/oftools_compile' + Context().tag + Context(
        ).time_stamp() + '.csv'
        report_name = os.path.expandvars(
            os.path.join(Context().root_workdir(), report_name))

        # Write results to the file
        with open(report_name, 'w') as fd:
            fd.write('source,list_dir,section,success,time')

            for record in self._records:
                result = record.to_csv()
                fd.write("%s\n" % result)

        # Inform the user that the report has been successfully generated
        Log().logger.info('CSV report successfully generated: ' + report_name)