#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log


class Job(object):
    """

    Attributes:
        _section_name:
        _filter_name:
        _section_no_filter:
        _profile:

    Methods:
        __init__(section_name, profile):
        _initialize_file_variables(file_path_in):
        _update_context():
        _analyze_common_options(key, value):
        _clear():
    """

    def __init__(self, section_name, profile):
        """
        """
        self._section_name = section_name
        self._profile = profile

        if '?' in self._section_name:
            self._section_no_filter = section_name.split('?')[0]
            self._filter_name = section_name.split('?')[1]
        else:
            self._filter_name = ''
            self._section_no_filter = self._section_name

        self._file_path_in = ''
        self._file_name_in = ''
        self._file_name_out = ''

    def _initialize_file_variables(self, file_path_in):
        """Detect if the source provided is a file or a directory, and properly retrieve the name of the file.

        Raises:
        """
        self._file_path_in = file_path_in

        try:
            self._file_name_in = file_path_in.rsplit('/', 1)[1]
        except IndexError:
            Log().logger.debug('A file has been specified, not a directory.')

        self._file_name_out = self._file_name_in

    def _update_context(self):
        """
        """
        base_file_name = self._file_name_out.rsplit('.', 1)[1]

        Context().add_env_variable('$OF_COMPILE_IN', self._file_name_in)
        Context().add_env_variable('$OF_COMPILE_OUT', self._file_name_out)
        Context().add_env_variable('$OF_COMPILE_BASE', base_file_name)

    def _analyze_common_options(self, key, value):
        """
        """
        if key.startswith('$'):
            Context().add_env_variable(key, value)
        elif key.startswith('?'):
            Context().add_filter(key, value)
        else:
            Log().logger.warning('Option not supported')

    def _clear(self):
        """
        """
        self._file_path_in = ''
        self._file_name_in = ''
        self._file_name_out = ''

