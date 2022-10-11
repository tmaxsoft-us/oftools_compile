#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to run the job for the profile deploy section.

Typical usage example:
  job = DeployJob()
  job.run(file_path_in)
"""
# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from ..Context import Context
from ..enums.LogEnum import LogMessage
from ..handlers.FileHandler import FileHandler
from ..handlers.ShellHandler import ShellHandler
from .Job import Job
from ..Log import Log


class DeployJob(Job):
    """A class used to perform all the steps of a deploy section.

    Attributes:
        Inherited from Job module.

    Methods:
        _analyze(): Analyzes prerequisites before running the job for the
            section.
        _process_section(): Read the section line by line to execute the
            corresponding methods.
        _process_file(option): Creates a new copy of the file based on the
            option value.
        _process_dataset(option): Runs the dlupdate command to deploy the
            compiled object.
        _process_region(option): Runs the osctdlupdate command to deploy the
            compiled object.
        _process_tdl(option): Runs the tdlupdate command to deploy the compiled
            object.
        run(file_path_in): Performs all the steps for the deploy section of the
            profile.
    """

    def _analyze(self):
        """Analyzes prerequisites before running the job for the section.

        It evaluates all the following elements:
            - is the section already complete, based on the name without the
                filter function
            - is the section mandatory, list of sections in the setup section
            - is the filter of the section True or False, if there is one
            - is any of the compile section complete

        Returns:
            integer -- Return code of the analysis.
        """
        filter_function = Context().get_filter_function(self._filter)

        if self._profile.is_section_complete(self._section_name):
            return_code = 1
        elif self._profile.is_section_mandatory(self._section_name):
            return_code = 0
        elif ShellHandler().evaluate_filter(filter_function, self._filter,
                                            self._section_name,
                                            Context().env) in (True, None):
            return_code = 0
        else:
            return_code = 1

        if return_code == 0:
            compile_section = False
            complete_status = False

            for key, value in self._profile.sections_complete.items():
                if key not in ("setup", "deploy"):
                    compile_section = True
                    complete_status = value
                    break

            if compile_section is True:
                Log().logger.debug(LogMessage.COMPILE_FOUND.value %
                                   self._section_name)
                if complete_status is True:
                    return_code = 0
                    Log().logger.debug(LogMessage.COMPLETE_FOUND.value %
                                       self._section_name)
                else:
                    return_code = -1
                    Log().logger.error(LogMessage.COMPLETE_NOT_FOUND.value %
                                       self._section_name)
            else:
                return_code = 0
                Log().logger.debug(LogMessage.COMPILE_NOT_FOUND.value %
                                   self._section_name)

        return return_code

    def _process_section(self):
        """Read the section line by line to execute the corresponding methods.

        For the deploy section, it analyzes either file, dataset, region or tdl
        options to find where to deploy the compiled program. And as any other
        section, it looks for environment and filter variables.

        Returns:
            integer - Return code of the method.
        """
        return_code = 0
        Log().logger.debug(LogMessage.START_SECTION.value %
                           (self._section_name, self._file_path_in))

        # file option must be processed first
        value = self._profile.data.get(self._section_name, "file")
        return_code = self._process_file(value)
        if return_code < 0:
            Log().logger.error(LogMessage.ABORT_SECTION.value %
                               (self._section_name, "file"))
            return return_code

        for key, value in self._profile.data[self._section_name].items():
            if key == "file":
                continue
            if key == "dataset":
                return_code = self._process_dataset(value)
            elif key == "region":
                return_code = self._process_region(value)
            elif key == "tdl":
                return_code = self._process_tdl(value)
            else:
                return_code = self._process_option(key, value)

            if return_code not in (0, 1):
                Log().logger.error(LogMessage.ABORT_SECTION.value %
                                   (self._section_name, key))
                break

        if return_code in (0, 1):
            Log().logger.debug(LogMessage.END_SECTION.value %
                               (self._section_name, self._file_name_out))
            self._profile.section_completed(self._section_no_filter)

        return return_code

    def _process_file(self, option):
        """Creates a new copy of the file based on the option value.

        Arguments:
            option {string} -- Value of the file option.

        Returns:
            integer -- Return code of the file processing.
        """
        Log().logger.debug(LogMessage.START_DEPLOY_FILE.value %
                           self._section_name)

        self._file_name_out = os.path.expandvars(option)

        Log().logger.info(
            LogMessage.CP_COMMAND.value %
            (self._section_name, self._file_name_in, self._file_name_out))
        return_code = FileHandler().copy_file(self._file_name_in, self._file_name_out)

        if return_code == 1:
            Log().logger.warning(LogMessage.FILE_ALREADY_EXISTS.value %
                                 (self._section_name, self._file_name_out))

        Log().logger.debug(LogMessage.END_DEPLOY_FILE.value %
                           self._section_name)

        return return_code

    def _process_dataset(self, option):
        """Runs the dlupdate command to deploy the compiled object.

        Arguments:
            option {string} -- Value of the dataset option.

        Returns:
            integer -- Return code of the dataset processing.
        """
        Log().logger.debug(LogMessage.START_DATASET.value % self._section_name)

        return_code = 0
        datasets = option.split(":")

        for dataset in datasets:
            if dataset != "":
                shell_command = "dlupdate " + Context(
                ).current_workdir + "/" + self._file_name_out + " " + dataset
                Log().logger.info(LogMessage.RUN_COMMAND.value %
                                  (self._section_name, shell_command))
                _, _, return_code = ShellHandler().execute_command(
                    shell_command, "deploy",
                    Context().env)
                if return_code != 0:
                    break
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     (self._section_name, "dataset"))
                return_code = 1

        Log().logger.debug(LogMessage.END_DATASET.value % self._section_name)

        return return_code

    def _process_region(self, option):
        """Runs the osctdlupdate command to deploy the compiled object.

        Arguments:
            option {string} -- Value of the region option.

        Returns:
            integer -- Return code of the region processing.
        """
        Log().logger.debug(LogMessage.START_REGION.value % self._section_name)

        return_code = 0
        regions = option.split(":")

        for region in regions:
            if region != "":
                region = os.path.expandvars(region)
                region_path = os.path.join("$OPENFRAME_HOME/osc/region",
                                           region + "/tdl/mod")
                return_code = FileHandler().copy_file(self._file_name_out, region_path)
                if return_code != 0:
                    break

                shell_command = "osctdlupdate " + region + " " + self._file_name_out
                Log().logger.info(LogMessage.RUN_COMMAND.value %
                                  (self._section_name, shell_command))
                _, _, return_code = ShellHandler().execute_command(
                    shell_command, "deploy",
                    Context().env)
                if return_code != 0:
                    break
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     (self._section_name, "region"))
                return_code = 1

        Log().logger.debug(LogMessage.END_REGION.value % self._section_name)

        return return_code

    def _process_tdl(self, option):
        """Runs the tdlupdate command to deploy the compiled object.

        Arguments:
            option {string} -- Value of the tdl option.

        Returns:
            integer -- Return code of the TDL processing.
        """
        Log().logger.debug(LogMessage.START_TDL.value % self._section_name)

        return_code = 0
        tdls = option.split(":")

        for tdl in tdls:
            if tdl != "":
                tdl = os.path.expandvars(tdl)
                tdl_path = os.path.join(tdl + "/tdl/mod")
                return_code = FileHandler().copy_file(self._file_name_out, tdl_path)
                if return_code != 0:
                    break

                shell_command = "tdlupdate -m " + self._file_name_out + " -r " + tdl_path
                Log().logger.info(LogMessage.RUN_COMMAND.value %
                                  (self._section_name, shell_command))
                _, _, return_code = ShellHandler().execute_command(
                    shell_command, "deploy",
                    Context().env)
                if return_code != 0:
                    break
            else:
                Log().logger.warning(LogMessage.VALUE_EMPTY.value %
                                     (self._section_name, "tdl"))
                return_code = 1

        Log().logger.debug(LogMessage.END_TDL.value % self._section_name)

        return return_code

    def run(self, file_path_in):
        """Performs all the steps for the deploy section of the profile.

        Returns:
            integer -- Return code of the deploy section.
        """
        self._initialize_file_variables(file_path_in)
        self._update_context()

        return_code = self._analyze()
        if return_code != 0:
            self._file_name_out = file_path_in
            return return_code

        return_code = self._process_section()
        if return_code not in (0, 1):
            self._file_name_out = file_path_in

        return return_code
