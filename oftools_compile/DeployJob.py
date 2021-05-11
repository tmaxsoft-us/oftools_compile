#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import shutil
import subprocess

# Third-party modules

# Owned modules
from .Context import Context
from .Job import Job
from .Log import Log
from .Utils import Utils


class DeployJob(Job):
    """

    Attributes:
        Inherited from Job module.

    Methods:
        _process_region(out_name):
        _process_tdl(out_name):
        _process_dataset(out_name):
        _process_file(out_name):
        run(file_path_in):
    """

    def _process_region(self, out_name):
        """
        """
        if self._profile.has_option(self._section_name, 'region') is False:
            return

        regions = self._profile.get(self._section_name, 'region').split(':')
        for region in regions:
            shell_cmd = 'cp ' + out_name + ' ' + os.path.join(
                '$OPENFRAME_HOME/osc/region',
                os.path.expandvars(region) + '/tdl/mod')
            shell_cmd += '; '
            shell_cmd += 'osctdlupdate'
            shell_cmd += ' ' + region
            #shell_cmd += ' ' + self._remove_extension_name(out_name)
            shell_cmd += ' ' + out_name

            Log().logger.info('[' + self._section_name + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle resultget
            if proc.returncode != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(proc.returncode)

        return

    def _process_tdl(self, out_name):
        """
        """
        if self._profile.has_option(self._section_name, 'tdl') is False:
            return

        tdls = self._profile.get(self._section_name, 'tdl').split(':')
        for tdl in tdls:
            shell_cmd = 'cp ' + out_name + ' ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')
            shell_cmd += '; '
            shell_cmd += 'tdlupdate'
            #shell_cmd += ' -m ' + self._remove_extension_name(out_name)
            shell_cmd += ' -m ' + out_name
            shell_cmd += ' -r ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')

            Log().logger.info('[' + self._section_name + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle result
            if proc.returncode != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(proc.returncode)

        return

    def _process_dataset(self, out_name):
        """
        """
        out = ''
        err = ''

        if self._profile.has_option(self._section_name, 'dataset') is False:
            return

        datasets = self._profile.get(self._section_name, 'dataset').split(':')
        for dataset in datasets:
            shell_cmd = 'dlupdate ' + os.path.join(os.getcwd(),
                                                   out_name) + ' ' + dataset
            Log().logger.info('[' + self._section_name + '] ' + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle result
            if proc.returncode != 0:
                Log().logger.error(err.decode(errors='ignore'))
                Log().logger.error(out.decode(errors='ignore'))
                exit(proc.returncode)

        return

    def _process_file(self, in_name):
        """
        """
        out_name = in_name

        try:
            out_name = self._profile.get(self._section_name, 'file')
            out_name = os.path.expandvars(out_name)

            if in_name != out_name:
                Log().logger.info('[' + self._section_name + '] ' + 'cp ' + in_name +
                                  ' ' + out_name)
                shutil.copy(in_name, out_name)

        except:
            Log().logger.error('[' + self._section_name + '] failed to copy ' +
                               in_name)
            exit(-1)

        return out_name

    def run(self, file_path_in):
        """
        """
        # Check if any compile job was successful
        if Context().is_mandatory_section_complete() is False:
            Log().logger.error(
                'mandatory section [' + Context().mandatory_section() +
                '] did not ran successfully. aborting the deploy job')
            #? We really need to exit here?
            exit(-1)
        # Analyze prerequisites before running the job for the section
        # Include completion of section and filter evaluation if there is one
        if self._is_section_complete() < 0 or self._filter_evaluation(
        ) == False:
            return file_path_in

        # start section
        Log().logger.debug('[' + self._section_name + '] start section')

        # update predefined environment variable
        base_name = Utils().remove_file_extension(file_path_in)
        out_name = base_name + '.' + self._profile.remove_filter(self._section_name)
        Context().add_env_variable('$OF_COMPILE_IN', file_path_in)
        Context().add_env_variable('$OF_COMPILE_OUT', out_name)
        Context().add_env_variable('$OF_COMPILE_BASE', base_name)

        # add environment variables
        for key in self._profile.options(self._section_name):
            value = self._profile.get(self._section_name, key)

            if key.startswith('$'):
                Context().add_env_variable(key, value)

        # process others
        out_name = self._process_file(file_path_in)
        self._process_dataset(out_name)
        self._process_tdl(out_name)
        self._process_region(out_name)

        # set section as completed
        Context().section_completed(self._profile._remove_filter(self._section_name))

        # end section
        Log().logger.debug('[' + self._section_name + '] end section')

        return out_name
