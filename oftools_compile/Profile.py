#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .Utils import Utils

class Profile():
    """

    Attributes:

    Methods:
        evaluate_filter(key):
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
                    filter_variable = option.replace('?','')
                    self._filter_variables[filter_variable] = self._data[section][option]

        if self._is_setup == False:
            print('Missign setup section in the profile.')
            exit(-1)
        if self._is_compile == False:
            print('Missing compile section in the profile.')
            exit(-1)

    def evaluate_filter(self, key):
        """
        """
        result = False
        index = key.find('?')
        if index > 0:
            key = key[index:]

        if key in Context().filters:
            result = Context().filters[key]

        return result