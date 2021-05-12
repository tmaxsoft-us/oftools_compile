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
        _is_section_completed():
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
            self._section_name_no_filter = section_name.split('?')[0]
            self._filter_name = section_name.split('?')[1]
        else:
            self._filter_name = ''
            self._section_name_no_filter = self._section_name

        self._file_path_in = ''
        self._file_name_in = ''
        self._file_name_out = ''

    def _is_section_complete(self):
        """Check if given section is already completed.
        """
        rc = 0
        if Context().is_section_complete(self._section_name_no_filter):
            Log().logger.debug(
                '[' + self._section_name_no_filter +
                '] section has already been processed. Skipping section')
            rc = -1
        else:
            rc = 0

        return rc

    def _filter_evaluation(self):
        """
        """
        if self._filter_name != '':
            filter_result = Context().evaluate_filter(self._filter_name)

            if filter_result == False:
                Log().logger.debug(
                    '[' + self._section_name + '] filter variable ' +
                    self._filter_name +
                    ' evaluation result: False. Skipping section')
        else:
            filter_result = None

        return filter_result

    def _initialize_file_variables(self, file_path_in):
        """Detect if the source provided is a file or a directory, and properly retrieve the name of the file.

        Raises:
        """
        self._file_path_in = file_path_in

        try:
            self._file_name_in = file_path_in.rsplit('/', 1)[1]
        except IndexError:
            Log().logger.debug('A file has been specified, not a directory.')

        if 'setup' in self._section_name or 'deploy' in self._section_name:
            self._file_name_out = self._file_name_in
        else:
            filename = self._file_name_in.rsplit('.', 1)[0]
            extension = self._section_name_no_filter
            self._file_name_out = filename + '.' + extension


    def _update_context(self):
        """
        """
        base_file_name = self._file_name_out.rsplit('.', 1)[0]

        Context().add_env_variable('$OF_COMPILE_IN', self._file_name_in)
        Context().add_env_variable('$OF_COMPILE_OUT', self._file_name_out)
        Context().add_env_variable('$OF_COMPILE_BASE', base_file_name)

    def _process_option(self, key, value):
        """
        """
        if key.startswith('$'):
            Context().add_env_variable(key, value)
        elif key.startswith('?'):
            Context().add_filter(key, value)
        else:
            Log().logger.warning(key + ': option not supported')

    def _clear(self):
        """
        """
        self._file_path_in = ''
        self._file_name_in = ''
        self._file_name_out = ''

        #? If there are two ofcbpp section and we want to know which one has been completed, should we store the section name with the filter instead?
        Context().section_completed(self._section_name_no_filter)
        Log().logger.debug('[' + self._section_name + '] end section')
