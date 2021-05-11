#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of variables and parameters for compilation execution.

  Typical usage example:

  Context = Context()
"""

# Generic/Built-in modules
import datetime
import os
import subprocess

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


class Context(metaclass=SingletonMeta):
    """A class used to store a set of variables and parameters across all modules.

    Attributes:
        _init_env: A dictionary,
        _env: A dictionary,

        _filters: A dictionary,
        _filter_results: A dictionary,

        _root_workdir: A string,
        _current_workdir: A string,
        _work_directories: A list,

        _mandatory_section: A string,
        _complete_sections: A dictionary,

        _tag: A string,
        _time_stamp: A string,

        _init_pwd: A string,

    Methods:
        __init(): Initializes all attributes of the class.
    """

    def __init__(self):
        """Initializes all attributes of the class.
        """
        # Environment
        self._init_env = os.environ.copy()
        self._env = self._init_env

        # Filter variables
        self._filters = {}
        self._filter_results = {}

        # Directories
        self._root_workdir = ''
        self._current_workdir = ''
        self._work_directories = []

        # Profile sections
        self._mandatory_section = ''
        self._complete_sections = {}

        # Tag
        self._tag = ''
        # Timestamp
        self._time_stamp = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')

        # Other
        self._init_pwd = os.getcwd()

    @property
    def env(self):
        """Getter method for the dictionary env, containing environment variables.
        """
        return self._env

    @property
    def filters(self):
        """Getter method for the dictionary filters, containing filter variables.
        """
        return self._filters

    @property
    def filter_results(self):
        """
        """
        return self._filter_results

    @property
    def root_workdir(self):
        """
        """
        return self._root_workdir

    @root_workdir.setter
    def root_workdir(self, workdir):
        """
        """
        self._root_workdir = workdir

    @property
    def current_workdir(self):
        """
        """
        return self._current_workdir

    @current_workdir.setter
    def current_workdir(self, workdir):
        """
        """
        self._current_workdir = workdir

    @property
    def work_directories(self):
        """
        """
        return self._work_directories

    #? What mandatory is used for? Figured it out by yourself!
    @property
    def mandatory_section(self):
        """
        """
        return self._mandatory_section

    @mandatory_section.setter
    def mandatory_section(self, section):
        """
        """
        index = section.find('?')
        if index > 0:
            section = section[:index]
        self._mandatory_section = section

    @property
    def complete_sections(self):
        """
        """
        return self._complete_sections

    @complete_sections.setter
    def add_complete_sections(self, value):
        self._complete_sections = value

    @property
    def tag(self):
        """
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """
        """
        if tag is not None:
            self._tag = '_' + tag

    @property
    def time_stamp(self):
        """
        """
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self, update):
        """
        """
        if update == 1:
            self._time_stamp = datetime.datetime.now().strftime(
                '_%Y%m%d_%H%M%S')

    def add_env_variable(self, key, value):
        """
        """
        if key.startswith('$'):
            if value.startswith('`') and value.endswith('`'):
                # value = value[value.find('`') + 1:value.rfind('`')]
                value = value[1:-1]
                proc = subprocess.Popen([value],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True,
                                        env=self._env)
                out, _ = proc.communicate()
                value = out.decode(errors='ignore').rstrip()
                self._env[key[1:]] = value
            else:
                self._env[key[1:]] = os.path.expandvars(value)

        os.environ.update(self._env)

    def add_filter(self, key, value):
        """
        """
        self._filters[key] = value
        self._filter_results[key] = False

    def evaluate_filter(self, key):
        """
        """
        filter_result = False
        shell_command = self._filters[key]

        # Filter evaluation
        out, err, rc = Utils().execute_shell_command(shell_command, self._env)

        #? What is it for?
        if out != b'':
            Log().logger.debug(err.decode(errors='ignore'))
        if err != b'':
            Log().logger.debug(out.decode(errors='ignore'))

        # grep command returns 0 if line matches
        if rc == 0:
            filter_result = True
        else:
            filter_result = False

        self._filter_results[key] = filter_result

        return filter_result

    def add_workdir(self):
        """
        """
        self._work_directories.append(self._cur_workdir)

    def section_completed(self, section):
        """
        """
        self._complete_sections[section] = True

    def is_mandatory_section_complete(self):
        """
        """
        return self._complete_sections[self.mandatory_section]

    def is_section_complete(self, section):
        """
        """
        return self._complete_sections[section]

    def clear(self):
        """
        """
        self._env = self._init_env
        os.environ.update(self._init_env)

        self._cur_workdir = ''
        self._mandatory_section = ''

        self._complete_sections.clear()
        self._filters.clear()

        os.chdir(self._init_pwd)
