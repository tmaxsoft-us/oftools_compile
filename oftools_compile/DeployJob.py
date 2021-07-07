#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to run the job for the deploy section of the profile.

  Typical usage example:

  job = DeployJob()
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
from .Utils import Utils


class DeployJob(Job):
    """A class used to perform all the steps of a deploy section.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze(): Analyzes prerequisites before running the job for the section.
        _process_section(): Read the section line by line to execute the corresponding methods.
        _process_file(option): Creates a new copy of the file with the given extension.
        _process_dataset(option): Runs the dlupdate shell command to deploy the compiled object.
        _process_region(option): Runs the osctdlupdate shell command to deploy the compiled object.
        _process_tdl(option): Runs the tdlupdate shell command to deploy the compiled object.
        run(file_path_in): Performs all the steps for the deploy section of the profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates all the following elements:
            - is the section already complete, based on the name without the filter variable
            - is the section mandatory, list of sections in the setup section
            - is the filter of section True or False, if there is one
            - is any of the compile section complete

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

        compile_section = False
        completion_status = False

        for key, value in Context().complete_sections.items():
            if key not in ('setup', 'deploy'):
                compile_section = True
                completion_status = value
                break

        if compile_section is True:
            Log().logger.debug(
                '[' + self._section_name +
                '] Compile section found. Evaluating completion status')
            if completion_status is True:
                rc = 0
                Log().logger.debug(
                    '[' + self._section_name +
                    '] Complete compile section found. Proceeding deploy job execution'
                )
            else:
                rc = -1
                Log().logger.error(
                    '[' + self._section_name +
                    '] None of the compile section is complete. Aborting deploy job execution'
                )
        else:
            rc = 0
            Log().logger.debug('[' + self._section_name +
                               '] No compile section found. Deploying only')

        return rc

    def _process_section(self):
        """Read the section line by line to execute the corresponding methods.

        For the deploy section, it analyzes either file, dataset, region or tdl options to find where 
        to deploy the compiled program. And as any other section, it looks for environment and filter 
        variables.

        Returns:
            An integer, the return code of the section execution.
        """
        rc = 0
        Log().logger.debug('[' + self._section_name +
                           '] Starting section, input filename: ' +
                           self._file_path_in)
        Context().last_section = self._section_name

        # file option must be processed first
        value = self._profile.get('deploy', 'file')
        rc = self._process_file(value)
        if rc < 0:
            Log().logger.error(
                '[' + self._section_name +
                '] Step failed: file. Aborting section execution')
            return rc

        for key, value in self._profile[self._section_name].items():
            if key == 'file':
                continue
            if key == 'dataset':
                rc = self._process_dataset(value)
            elif key == 'region':
                rc = self._process_region(value)
            elif key == 'tdl':
                rc = self._process_tdl(value)
            else:
                rc = self._process_option(key, value)

            if rc < 0:
                Log().logger.error('[' + self._section_name +
                                   '] Step failed: ' + key +
                                   '. Aborting section execution')
                break

        if rc >= 0:
            Log().logger.debug('[' + self._section_name +
                               '] Ending section, output filename: ' +
                               self._file_name_out)
            Context().section_completed(self._section_name_no_filter)

        return rc

    def _process_file(self, option):
        """Creates a new copy of the file with the given extension.

        Returns:
            An integer, the return code of the file processing.
        """
        Log().logger.debug('[' + self._section_name + '] Processing file')

        self._file_name_out = os.path.expandvars(option)

        try:
            shutil.copy(self._file_name_in, self._file_name_out)
            rc = 0
            Log().logger.info('[' + self._section_name + '] cp ' +
                              self._file_name_in + ' ' + self._file_name_out)
        except shutil.SameFileError:
            rc = 0
            Log().logger.warning('[' + self._section_name +
                                 '] No copy required, file already exists')
        except OSError as e:
            rc = -1
            Log().logger.error('[' + self._section_name +
                               '] Failed to copy: %s' % e)

        return rc

    def _process_dataset(self, option):
        """Runs the dlupdate shell command to deploy the compiled object.

        Returns:
            An integer, the return code of the dlupdate command executed.
        """
        rc = 0
        Log().logger.debug('[' + self._section_name + '] Processing dataset(s)')

        datasets = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for dataset in datasets:
            if dataset != '':
                shell_command = 'dlupdate ' + file_path_out + ' ' + dataset
                Log().logger.info('[' + self._section_name + '] ' +
                                  shell_command)
                _, _, rc = Utils().execute_shell_command(
                    shell_command, 'deploy',
                    Context().env)
                if rc < 0:
                    break

        return rc

    def _process_region(self, option):
        """Runs the osctdlupdate shell command to deploy the compiled object.

        Returns:
            An integer, the return code of the osctdlupdate command executed.
        """
        rc = 0
        Log().logger.debug('[' + self._section_name + '] Processing region(s)')

        regions = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for region in regions:
            if region != '':
                region_path = os.path.join(
                    '$OPENFRAME_HOME/osc/region',
                    os.path.expandvars(region) + '/tdl/mod')
                shell_command = 'cp ' + file_path_out + ' ' + region_path
                Log().logger.info('[' + self._section_name + '] ' +
                                  shell_command)
                _, _, rc = Utils().execute_shell_command(
                    shell_command, 'deploy',
                    Context().env)
                if rc < 0:
                    break

                shell_command = 'osctdlupdate ' + region + ' ' + self._file_name_out
                Log().logger.info('[' + self._section_name + '] ' +
                                  shell_command)
                _, _, rc = Utils().execute_shell_command(
                    shell_command, 'deploy',
                    Context().env)
                if rc < 0:
                    break

        return rc

    def _process_tdl(self, option):
        """Runs the tdlupdate shell command to deploy the compiled object.

        Returns:
            An integer, the return code of the tdlupdate command executed.
        """
        rc = 0
        Log().logger.debug('[' + self._section_name + '] Processing tdl(s)')

        tdls = option.split(':')
        file_path_out = os.path.join(os.getcwd(), self._file_name_out)

        for tdl in tdls:
            if tdl != '':
                tdl_path = os.path.join(os.path.expandvars(tdl) + '/tdl/mod')
                shell_command = 'cp ' + file_path_out + ' ' + tdl_path
                Log().logger.info('[' + self._section_name + '] ' +
                                  shell_command)
                _, _, rc = Utils().execute_shell_command(
                    shell_command, 'deploy',
                    Context().env)
                if rc < 0:
                    break

                shell_command = 'tdlupdate -m ' + file_path_out + ' -r ' + tdl_path
                Log().logger.info('[' + self._section_name + '] ' +
                                  shell_command)
                _, _, rc = Utils().execute_shell_command(
                    shell_command, 'deploy',
                    Context().env)
                if rc < 0:
                    break

        return rc

    def run(self, file_path_in):
        """Performs all the steps for the deploy section of the profile.

        Returns:
            An integer, the return code of the deploy section.
        """
        self._initialize_file_variables(file_path_in)
        self._update_context()

        rc = self._analyze()
        if rc != 0:
            self._file_name_out = file_path_in
            return rc

        rc = self._process_section()
        if rc != 0:
            self._file_name_out = file_path_in
            return rc

        return rc
