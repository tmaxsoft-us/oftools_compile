#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import shutil
from datetime import datetime

# Third-party modules

# Owned modules
from .Job import Job
from .Log import Log
from .Context import Context


class SetupJob(Job):

    def _analyze(self):

        # check if workdir is defined in the profile
        if self._profile.has_option(self._section, 'workdir') is False:
            Log().get().critical('cannot find workdir section in the profile')
            exit(-1)

        # check if workdir is accessable
        workdir = self._profile.get(self._section, 'workdir')
        workdir = os.path.expandvars(workdir)
        if os.path.isdir(workdir) is False:
            if os.access(workdir, os.W_OK) is False:
                Log().get().critical('no write access on workdir = ' + workdir)
                exit(-1)

        # check if given section is already completed
        if Context().is_section_complete(self._section):
            return -1

        return 0

    def _process_workdir(self, workdir, in_name):

        # Create the name for the workdir by adding suffix to in_name
        workdir = os.path.expandvars(workdir)
        Context().set_root_workdir(workdir)

        try:
            file_name = in_name.rsplit('/', 1)[1]
        except:
            file_name = in_name

        cur_workdir = os.path.join(workdir,
                                   file_name + Context().get_time_stamp())

        # create_workdir
        if not os.path.isdir(cur_workdir):
            os.mkdir(cur_workdir)

        # create_reportdir
        report_workdir = os.path.join(workdir, 'report')
        if not os.path.isdir(report_workdir):
            os.mkdir(report_workdir)

        # set log file handle
        Log().set_file(os.path.join(workdir, 'oftools_compile.out'))
        Log().get().info(
            '===================================================================================================='
        )
        Log().get().info('| [' + self._section + '] ' + 'source: ' + in_name)
        Log().get().info('| [' + self._section + '] ' + 'mkdir ' + cur_workdir)

        # copy source to workdir
        shutil.copy(in_name, cur_workdir)

        # change directory to workdir
        os.chdir(cur_workdir)
        Context().set_cur_workdir(cur_workdir)

        return file_name

    def run(self, in_name):
        # analyze section
        if self._analyze() < 0:
            Log().get().debug("[" + self._section + "] skip section")
            return in_name

        # start section
        Log().get().debug("[" + self._section + "] start section")

        # add environment variables and filters
        for key in self._profile.options(self._section):
            value = self._profile.get(self._section, key)

            if key.startswith('$'):
                Context().add_env(key, value)

            elif key.startswith('?'):
                self._add_filter(key, value, in_name)

        # process workdir
        key = self._profile.get(self._section, 'workdir')
        out_name = self._process_workdir(key, in_name)

        # set the mandatory section
        sections = self._profile.sections()
        for section in reversed(sections):
            if section.startswith('deploy') is False:
                Log().get().debug('mandatory section? ' + section)
                Context().set_mandatory_section(section)
                break

        # update predefined environment variable
        base_name = self._resolve_base_name(out_name)
        Context().add_env('$OF_COMPILE_IN', out_name)
        Context().add_env('$OF_COMPILE_OUT', out_name)
        Context().add_env('$OF_COMPILE_BASE', base_name)

        # set setup section as completed
        Context().set_section_complete(self._section)

        # end section
        Log().get().debug("[" + self._section + "] end section")

        return out_name
