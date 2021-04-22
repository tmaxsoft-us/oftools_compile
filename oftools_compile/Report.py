#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
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

    def __init__(self, source, list_dir, section, success, unit_time):
        self._source = source
        self._section = section
        self._success = success
        self._list_dir = list_dir
        self._unit_time = unit_time
        pass

    def to_csv(self):
        return str(self._source + ',' + self._list_dir + ',' + self._section +
                   ',' + self._success + ',' + str(round(self._unit_time, 4)))


class Report(object):

    _total_time = 0
    _success_count = 0
    _fail_count = 0
    _records = []

    def __init__(self):
        return

    def add_entry(self, source, last_job, return_code, elapsed_time):

        # Is the compilation a success or a failure?
        if return_code >= 0:
            compilation_status = 'S'
            self._success_count += 1
        else:
            compilation_status = 'F'
            self._fail_count += 1

        # Retrieve section corresponding to the latest job for the report
        last_section = last_job._remove_filter_name(last_job.section)
        #? Still mandatory section?????????
        if last_section.startswith('deploy'):
            if Context().is_mandatory_section_complete() is False:
                last_section = Context().mandatory_section

        record = Record(source, Context().current_workdir, last_section, compilation_status,
                        elapsed_time)
        self._records.append(record)

        self._total_time += elapsed_time

        if return_code >= 0:
            Log().get().info('BUILD SUCCESS (' + str(round(elapsed_time, 4)) +
                             ' sec)')
        else:
            Log().get().info('BUILD FAILED (' + str(round(elapsed_time, 4)) +
                             ' sec)')
        Log().get().info('')

        return

    def generate(self):

        results = []
        results.append("source,list_dir,section,success,time")

        Log().get().info(
            '= SUMMARY ==================================================')
        Log().get().info('TOTAL TIME: ' + str(round(self._total_time, 4)) +
                         ' sec')
        Log().get().info('TOTAL     : ' +
                         str(self._success_count + self._fail_count))
        Log().get().info('SUCCESS   : ' + str(self._success_count))
        Log().get().info('FAILED    : ' + str(self._fail_count))

        for record in self._records:
            results.append(record.to_csv())

        # export the report file
        file_name = 'report/oftools_compile' + Context().tag() + Context(
        ).time_stamp() + '.csv'
        file_name = os.path.expandvars(
            os.path.join(Context().root_workdir(), file_name))

        with open(file_name, 'w') as f:
            for result in results:
                f.write("%s\n" % result)
        f.close()

        Log().get().info('csv report has been generated: ' + file_name)

        return