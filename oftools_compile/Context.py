#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of variables and parameters for program execution.

Typical usage example:
  Context().tag = args.tag
  Context().clear()
"""

# Generic/Built-in modules
import datetime
import os
import time

# Third-party modules

# Owned modules
from .Log import Log
from .Utils import Utils


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(object, metaclass=SingletonMeta):
    """A class used to store a set of variables and parameters across all modules.

    Attributes:
        _init_env: A dictionary, the output of the os.environ.copy method.
        _env: A dictionary, all the environment variables for the current execution of the program.

        _root_workdir: A string, the absolute path of the working directory for all compilations.
        _current_workdir: A string, the absolute path of the directory created for the program being 
            currently compiled.
        _work_directories: A list of strings, the absolute paths of all the working directories. 
        _group_directory: A string, the absolute path of the group directory if the grouping feature 
            is being used.

        _last_section: A string, the name of the last section being executed, whether it succeeds or 
            fails.
        _mandatory_section: A list, all the sections that are listed as mandatory.
        _complete_sections: A dictionary, the section names and their status as complete or not.

        _filters: A dictionary, filter names and their respective values.

        _report_file_path: A string, the absolute path of the report file of the compilation.

        _skip: A boolean, a flag used to skip source files if not found or not.        
        _tag: A string, a keyword to identify working directories and report for a given compilation.
        _time_stamp: A string, a datetime respecting _%Y%m%d_%H%M%S format for working directories and 
            report identification purposes.

        _init_pwd: A string, the initial directory where the command has been executed. 

    Methods:
        __init__(): Initializes all attributes of the class.
        add_env_variable(key, value): Adds a variable to the environment.
        add_filter(key, value): Adds a filter function to the list of filters.
        add_mandatory_section(section): Adds the input section name to mandatory sections list.

        evaluate_filter(section_name, filter_name): Evaluates the status of the filter function passed 
            as an argument.

        is_section_mandatory(section_name_no_filter): Checks if given section is mandatory or not.
        is_section_complete(section_name_no_filter, skip=True): Checks if given section is already 
            complete.
        section_completed(section_name_no_filter): Changes the status of the given section to complete.

        clear(): Clears context after each file processing.
        clear_all(): Clears context completely at the end of the program execution.
    """

    def __init__(self):
        """Initializes all attributes of the class.
        """
        # Environment
        self._init_env = os.environ.copy()
        self._env = self._init_env

        # Directories
        self._root_workdir = ''
        self._current_workdir = ''
        self._work_directories = []
        self._group_directory = ''

        # Profile sections
        self._last_section = ''
        self._mandatory_sections = []

        # Filter variables
        self._filters = {}

        # Report
        self._report_file_path = ''

        # Skip flag
        self._skip = False
        # Tag
        self._tag = ''
        # Timestamp
        self._time_stamp = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')

        # Other
        self._init_pwd = os.getcwd()

    @property
    def env(self):
        """Getter method for the attribute _env.
        """
        return self._env

    @property
    def root_workdir(self):
        """Getter method for the attribute _root_workdir.
        """
        return self._root_workdir

    @root_workdir.setter
    def root_workdir(self, workdir):
        """Setter method for the attribute _root_workdir.
        """
        self._root_workdir = workdir

    @property
    def current_workdir(self):
        """Getter method for the attribute _current_workdir.
        """
        return self._current_workdir

    @current_workdir.setter
    def current_workdir(self, workdir):
        """Setter method for the attribute _current_workdir.
        """
        self._current_workdir = workdir
        self._work_directories.append(workdir)

    @property
    def work_directories(self):
        """Getter method for the attribute _work_directories.
        """
        return self._work_directories

    @property
    def group_directory(self):
        """Getter method for the attribute _group_directory.
        """
        return self._group_directory

    @group_directory.setter
    def group_directory(self, directory):
        """Setter method for the attribute _group_directory.
        """
        self._group_directory = directory

    @property
    def last_section(self):
        """Getter method for the attribute _last_section.
        """
        return self._last_section

    @last_section.setter
    def last_section(self, section):
        """Setter method for the attribute _last_section.
        """
        self._last_section = section

    @property
    def mandatory_sections(self):
        """Getter method for the attribute _mandatory_sections.
        """
        return self._mandatory_sections

    @property
    def filters(self):
        """Getter method for the attribute _filters.
        """
        return self._filters

    @property
    def report_file_path(self):
        """Getter method for the attribute _report_file_path.
        """
        return self._report_file_path

    @report_file_path.setter
    def report_file_path(self, file_path):
        """Setter method for the attribute _report_file_path.
        """
        self._report_file_path = file_path

    @property
    def skip(self):
        """Getter method for the attribute _skip.
        """
        return self._skip

    @skip.setter
    def skip(self, skip):
        """Setter method for the attribute _skip.
        """
        if skip is not None:
            self._skip = skip

    @property
    def tag(self):
        """Getter method for the attribute _tag.
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Setter method for the attribute _tag.
        """
        if tag is None and self._skip is False:
            self._tag, _, _ = Utils().execute_shell_command('logname', 'init', self._env)
            self._tag = '_' + self._tag.replace('\n', '')
        else:
            self._tag = '_' + tag

    @property
    def time_stamp(self):
        """Getter method for the attribute _time_stamp.
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, update=0):
        """Setter method for the attribute _time_stamp.
        """
        time.sleep(1)
        if update == 1:
            self._time_stamp = datetime.datetime.now().strftime(
                '_%Y%m%d_%H%M%S')

    def add_env_variable(self, key, value):
        """Adds a variable to the environment.
        """
        if not value.startswith('$(') and not value.startswith('`'):
            self._env[key[1:]] = os.path.expandvars(value)
        else:
            if value.startswith('$(') and value.endswith(')'):
                value = value[2:-1]
            elif value.startswith('`') and value.endswith('`'):
                value = value[1:-1]
            out, _, _ = Utils().execute_shell_command(value, 'env_variable',
                                                      self._env)
            value = out.rstrip()
            # Write to env dictionary without dollar sign
            self._env[key[1:]] = value

        os.environ.update(self._env)

    def add_filter(self, key, value):
        """Adds a filter function to the list of filters.
        """
        # Write to filters dictionary without question mark
        self._filters[key[1:]] = value

    def add_mandatory_section(self, section):
        """Adds the input section name to mandatory sections list.
        """
        if '?' in section:
            Log().logger.warning(
                '[setup] Filter function not allowed in the mandatory sections: '
                + section)
            section_name_no_filter = section.split('?')[0]
        else:
            section_name_no_filter = section

        Log().logger.info('[setup] Adding section to mandatory sections: ' +
                          section_name_no_filter)
        self._mandatory_sections.append(section_name_no_filter)

    def evaluate_filter(self, section_name, filter_name):
        """Evaluates the status of the filter function passed as an argument.
        """
        if filter_name != '':
            filter_result = False
            shell_command = self._filters[filter_name]

            # Filter evaluation
            _, _, rc = Utils().execute_shell_command(shell_command, 'filter',
                                                     self._env)

            # grep command returns 0 if line matches
            if rc == 0:
                filter_result = True
                Log().logger.debug(
                    '[' + section_name + '] Filter function ' + filter_name +
                    ' result: True. Executing section.')
            else:
                filter_result = False
                Log().logger.debug(
                    '[' + section_name + '] Filter function ' + filter_name +
                    ' result: False. Skipping section.')
        else:
            filter_result = None

        return filter_result

    def is_section_mandatory(self, section_name_no_filter):
        """Checks if given section is mandatory or not.
        """
        if section_name_no_filter in self._mandatory_sections:
            mandatory_status = True
        else:
            mandatory_status = False

        return mandatory_status

    def is_section_complete(self, profile, section_name_no_filter, skip=True):
        """Checks if given section is already complete.
        """
        section_status = profile.complete_sections[section_name_no_filter]

        if section_status and skip is True:
            Log().logger.debug(
                '[' + section_name_no_filter +
                '] Section has already been processed. Skipping section')

        return section_status

    def section_completed(self, profile, section_name_no_filter):
        """Changes the status of the given section to complete.
        """
        profile.complete_sections[section_name_no_filter] = True

    def clear(self, profile):
        """Clears context after each file processing.
        """
        self._env = self._init_env
        os.environ.update(self._init_env)

        self._filters.clear()

        for key in profile.complete_sections.keys():
            profile.complete_sections[key] = False

        os.chdir(self._init_pwd)

    def clear_all(self):
        """Clears context completely at the end of the program execution.
        """
        self._root_workdir = ''
        self._current_workdir = ''
        self._work_directories = []
        self._group_directory = ''

        self._last_section = ''
        self._mandatory_sections = []

        os.chdir(self._init_pwd)
