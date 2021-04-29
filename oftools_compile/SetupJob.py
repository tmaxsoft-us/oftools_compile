#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import shutil
import time
import datetime

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class SetupJob(Job):
    """

    Methods:
        _analyze:
        _process_worldir(workdir, in_name):
        _run():
    """

    def _analyze(self):

        # check if workdir is defined in the profile
        if self._profile.has_option(self._section, 'workdir') is False:
            Log().logger.critical(
                '[' + self._section +
                '] cannot find workdir section in the profile')
            exit(-1)

        # check if workdir is accessable
        workdir = self._profile.get(self._section, 'workdir')
        workdir = os.path.expandvars(workdir)
        if os.path.isdir(workdir) is False:
            if os.access(workdir, os.W_OK) is False:
                Log().logger.critical('[' + self._section +
                                      '] no write access on workdir = ' +
                                      workdir)
                exit(-1)

        # check if given section is already completed
        if Context().is_section_complete(self._section):
            return -1

        return 0

    def _process_workdir(self, workdir, in_name):

        # Create the name for the workdir by adding suffix to in_name
        workdir = os.path.expandvars(workdir)
        Context().root_workdir(workdir)

        try:
            file_name = in_name.rsplit('/', 1)[1]
        except:
            file_name = in_name

        current_workdir = os.path.join(
            workdir, file_name + Context().tag() + Context().time_stamp())

        # create_workdir
        while True:
            if not os.path.isdir(current_workdir):
                os.mkdir(current_workdir)
                break

            Log().logger.warning(
                current_workdir +
                ' already exists. sleep 1 second to assign a new time stamp')
            time.sleep(1)
            Context().time_stamp(1)
            workdir = os.path.join(
                workdir, file_name + Context().tag() + Context().time_stamp())

        # create_reportdir
        report_workdir = os.path.join(workdir, 'report')
        if not os.path.isdir(report_workdir):
            os.mkdir(report_workdir)

        # copy source to workdir
        shutil.copy(in_name, current_workdir)

        # change directory to workdir
        os.chdir(current_workdir)
        Context().current_workdir(current_workdir)

        # set log file
        Log().open_file(
            os.path.join(Context().current_workdir, 'oftools_compile.log'))

        header = '============================================================'
        header = header[:1] + ' ' + file_name + ' ' + header[len(file_name) +
                                                             2:]

        Log().logger.info(header)
        Log().logger.info('[' + self._section + '] ' + 'mkdir ' +
                          current_workdir)
        Log().logger.info('[' + self._section + '] ' + 'cp ' + in_name + ' ' +
                          current_workdir)
        Log().logger.info('[' + self._section + '] ' + 'cd ' + current_workdir)

        return file_name

    def run(self, in_name):
        # analyze section
        if self._analyze() < 0:
            Log().logger.debug('[' + self._section + '] skip section')
            return in_name

        # update predefined environment variable
        try:
            out_name = in_name.rsplit('/', 1)[1]
        except:
            out_name = in_name
        base_name = Utils().remove_extension_name(out_name)
        Context().add_env_variable('$OF_COMPILE_IN', out_name)
        Context().add_env_variable('$OF_COMPILE_OUT', out_name)
        Context().add_env_variable('$OF_COMPILE_BASE', base_name)

        # add environment variables and filters
        Log().logger.debug('[' + self._section + '] process options')
        for key in self._profile.options(self._section):
            value = self._profile.get(self._section, key)

            if key.startswith('$'):
                Context().add_env_variable(key, value)

            elif key.startswith('?'):
                self._profile.evaluate_filter(self._section)

            elif key == 'workdir':
                out_name = self._process_workdir(value, in_name)

        # set the mandatory section
        sections = self._profile.sections()
        if 'deploy' in sections:
            for section in reversed(sections):
                if section.startswith('deploy') is False:
                    Log().logger.debug('[' + self._section +
                                       '] mandatory section: ' + section)
                    Context().mandatory_section(section)
                    break

        # set section as completed
        Context().section_completed(
            self._profile.remove_filter_name(self._section))

        return out_name
