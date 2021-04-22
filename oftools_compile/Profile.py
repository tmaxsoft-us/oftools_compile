#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log
from .Utils import Utils


class Profile():
    """

    Attributes:

    Methods:
        __init__():
        _analyze():
        is_filter(section):
        evaluate_filter(section):
        remove_filter(section):
    """

    def __init__(self, path_to_profile):
        """
        """
        self._data = Utils().read_file(path_to_profile)
        self._sections = self._data.sections()

        self._is_setup = False
        self._is_compile = False
        self._filter_variables = {}
        self._env_variables = {}

        self._analyze()
        self._add_env_variables_to_context()

    @property
    def data(self):
        """
        """
        return self._data

    @property
    def sections(self):
        """
        """
        return self._sections

    def _analyze(self):
        """
        """
        for section in self._sections:
            if section is None:
                #TODO Find proper implementation
                pass
            if section.startswith('setup'):
                self._is_setup = True
            elif section.startswith('deploy'):
                self._is_compile = True

            for option in self.data[section]:
                if option.startswith('$'):
                    self._env_variables[option] = self._data[section][option]
                elif option.startswith('?'):
                    filter_name = option.replace('?', '')
                    self._filter_variables[filter_name] = self._data[section][
                        option]

        if self._is_setup == False:
            print('Missing setup section in the profile.')
            exit(-1)
        if self._is_compile == False:
            print('Missing compile section in the profile.')
            exit(-1)

    def _add_env_variables_to_context(self):
        """
        """
        for key, value in self._env_variables.items():
            Context().add_env_variable(key, value)

    def is_filter(self, section):
        """
        """
        if '?' in section and 'setup' not in section:
            return True
        else:
            return False

    def evaluate_filter(self, section):
        """
        """
        filter_name = section.split('?')[1]
        filter_value = self._filter_variables[filter_name]

        env = Context().env()
        out, err, rc = Utils().execute_shell_command(filter_value, env)

        #? What is it for?
        if out != b'':
            Log().get().debug(err.decode(errors='ignore'))
        if err != b'':
            Log().get().debug(out.decode(errors='ignore'))

        # grep command returns 0 if line matches
        if rc == 0:
            result = True
        else:
            result = False

        return result

    def remove_filter(self, section):
        """
        """
        return section.split('?')[0]
