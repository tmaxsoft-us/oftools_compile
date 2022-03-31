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
import sys

# Third-party modules

# Owned modules
from .enums.ErrorEnum import ErrorMessage
from .enums.LogEnum import LogMessage
from .Log import Log
from .handlers.ShellHandler import ShellHandler


class SingletonMeta(type):
    """This pattern restricts the instantiation of a class to one object. 
    
    It is a type of creational pattern and involves only one class to create methods and specified objects. It provides a global point of access to the instance created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(object, metaclass=SingletonMeta):
    """A class used to store a set of variables and parameters across all modules.

    Attributes:
        _init_env {dictionary} -- Output of the os.environ.copy method.
        _env {dictionary} -- All the environment variables for the current execution of the program.

        _root_workdir {string} -- Absolute path of the root working directory.
        _current_workdir {string} -- Absolute path of the current working directory.
        _work_directories {list} -- Absolute paths of all the working directories. 
        _group_directory {string} -- Absolute path of the group directory.

        _last_section {string} -- Name of the last section being executed, whether it succeeds or 
            fails.
        _mandatory_section {list} -- Sections that are listed as mandatory.
        _complete_sections {dictionary} -- Section names and their status as complete or not.

        _filters {dictionary} -- Filter names and their respective values.

        _report_file_path {string} -- Absolute path of the report file of the compilation.

        _skip {boolean} -- Flag used to skip source files if not found or not.        
        _tag {string} -- Keyword to tag working directories and report file.
        _time_stamp {string} -- Datetime respecting _%Y%m%d_%H%M%S format for working directories and 
            report identification purposes.

        _init_pwd {string} -- Absolute path of the initial directory where the command has been executed. 

    Methods:
        __init__() -- Initializes all attributes of the class.
        add_env_variable(key, value) -- Adds a variable to the environment.
        add_filter(key, value) -- Adds a filter function to the list of filters.
        get_filter_function(key) -- Retrieves the expression of the filter function from the Context.
        add_mandatory_section(section) -- Adds the input section name to mandatory sections list.

        is_section_mandatory(section_name_no_filter) -- Checks if given section is mandatory or not.
        is_section_complete(section_name_no_filter, skip=True) -- Checks if given section is already 
            complete.
        section_completed(section_name_no_filter) -- Changes the status of the given section to complete.

        clear() -- Clears context after each file processing.
        clear_all() -- Clears context completely at the end of the program execution.
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
        self._complete_sections = {}

        # Filter variables
        self._filters = {}

        # Report
        self._report_file_path = ''

        # Skip flag
        self._skip = False
        # Tag
        self._tag = ''
        # Timestamp
        self._time_stamp = datetime.datetime.now()

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
        self._root_workdir = os.path.expandvars(workdir)

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
    def complete_sections(self):
        """Getter method for the attribute _complete_sections.
        """
        return self._complete_sections

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
        if tag is None:
            self._tag, _, _ = ShellHandler().execute_command(
                'logname', 'tag', self._env)
            self._tag = '_' + self._tag.replace('\n', '')
        else:
            self._tag = '_' + tag

    @property
    def time_stamp(self):
        """Getter method for the attribute _time_stamp.
        """
        return self._time_stamp.strftime('_%Y%m%d_%H%M%S')

    @time_stamp.setter
    def time_stamp(self, update):
        """Setter method for the attribute _time_stamp.

        Arguments:
            update {integer} -- Number of seconds needed to update the time stamp.
        """
        time_update = datetime.timedelta(seconds=update)
        self._time_stamp += time_update

    def add_env_variable(self, key, value):
        """Adds a variable to the environment.

        Arguments:
            key {string} -- Name of the environment variable.
            value {string} -- Value of the environment variable.
        """
        if not value.startswith('$(') and not value.startswith('`'):
            self._env[key[1:]] = os.path.expandvars(value)
        else:
            if value.startswith('$(') and value.endswith(')'):
                value = value[2:-1]
            elif value.startswith('`') and value.endswith('`'):
                value = value[1:-1]
            out, _, _ = ShellHandler().execute_command(value, 'env_variable',
                                                       self._env)
            value = out.rstrip()
            # Write to env dictionary without dollar sign
            self._env[key[1:]] = value

        os.environ.update(self._env)

    def add_filter(self, key, value):
        """Adds a filter function to the list of filters.

        Arguments:
            key {string} -- Name of the filter function.
            value {string} -- Expression of the filter function.
        """
        # Remove question mark from filter function name
        self._filters[key[1:]] = value

    def get_filter_function(self, key):
        """Retrieves the expression of the filter function from the Context.

        Arguments:
            key {string} -- Name of the filter function.

        Returns:
            string -- Expression of the filter function.

        Raises:
            KeyError -- Exception raised if a filter function is used in the profile before being defined.
        """
        try:
            if key == '':
                filter_function = ''
            else:
                filter_function = self.filters[key]
        except KeyError:
            Log().logger.error(ErrorMessage.KEY_FILTER.value % key)
            self.clear_all()
            sys.exit(-1)

        return filter_function

    def add_mandatory_section(self, section_no_filter):
        """Adds the input section name to mandatory sections list.

        Arguments:
            section {string} -- Name of the section.
        """
        Log().logger.info(LogMessage.MANDATORY_ADD.value % section_no_filter)
        self._mandatory_sections.append(section_no_filter)

    def is_section_mandatory(self, section, section_no_filter):
        """Checks if given section is mandatory or not.

        Arguments:
            section {string} -- Name of the section.
            section_no_filter {string} -- Name of the section without filter.

        Returns:
            boolean -- Status of the section, if it is mandatory or not.
        """
        if section_no_filter in self._mandatory_sections:
            Log().logger.debug(LogMessage.SECTION_MANDATORY.value % section)
            mandatory_status = True
        else:
            mandatory_status = False

        return mandatory_status

    def is_section_complete(self, section, section_no_filter, skip=True):
        """Checks if given section is already complete.

        Arguments:
            section {string} -- Name of the section.
            section_no_filter {string} -- Name of the section without filter.
            skip {boolean} -- Value of the skip flag.

        Returns:
            boolean -- Status of the section, if it is completer or not.
        """
        section_status = self._complete_sections[section_no_filter]

        if section_status and skip is True:
            Log().logger.debug(LogMessage.SECTION_COMPLETE.value % section)

        return section_status

    def section_completed(self, section_no_filter):
        """Changes the status of the given section to complete.

        Arguments:
            section_no_filter {string} -- Name of the section without filter.
        """
        self._complete_sections[section_no_filter] = True

    def clear(self):
        """Clears context after each file processing.
        """
        self._env = self._init_env
        os.environ.update(self._init_env)

        self._filters.clear()
        for key in self._complete_sections.keys():
            self._complete_sections[key] = False

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
        self._complete_sections.clear()

        os.chdir(self._init_pwd)
