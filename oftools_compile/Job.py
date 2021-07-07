#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Common module for all Job modules in this program.

Typical usage example:
  job = Job(setup, profile)
  job.run()
  file_name_out = job.file_name_out
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log


class Job(object):
    """A class used to store common values and execute common methods to all type of jobs.

    Attributes:
        _section_name: A string, the name of the section in the profile.
        _profile: A Profile object, from the Profile module.
        _section_name_no_filter: A string, the name of the section without the filter if there is one.
        _filter_name: A string, if there is one it is the name of the filter extracted from the name of 
            the section.
        _file_path_in: A string, the absolute path of the input file. It could also be just the file 
            name, depending on the type of job.
        _file_name_in: A string, the input file name.
        _file_name_out: A string, the output file name.

    Methods:
        __init__(section_name, profile): Initializes the class with all the attributes.
        _initialize_file_variables(file_path_in): Detects if the source provided is a file or a 
            directory, and properly retrieve the name of the file to initialize class attributes.
        _update_context(): Updates Context with name of files being manipulated in this job execution.
        _process_option(key, value): Processes option like environment or filter variable.
    """

    def __init__(self, section_name, profile):
        """Initializes the class with all the attributes.
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

    @property
    def file_name_out(self):
        """Getter method for the attribute _file_name_out.
        """
        return self._file_name_out

    def _initialize_file_variables(self, file_path_in):
        """Detects if the source provided is a file or a directory, and properly retrieve the name of 
        the file to update class attributes.

        Args:
            file_path_in: A string, the absolute path of the input file. It could also be just the file 
                name, depending on the type of job.

        Raises:
            IndexError: An error occurs if there is no '/' symbol in the file name, which means only 
                the file name has been provided and not the absolute file path.
        """
        # Initialize file_path_in
        self._file_path_in = file_path_in
        # Initializes file_name_in
        try:
            self._file_name_in = self._file_path_in.rsplit('/', 1)[1]
        except IndexError:
            # Log().logger.debug(
            #     '[' + self._section_name +
            #     '] A file has been specified, not a path to the file')
            self._file_name_in = self._file_path_in
        # Initialize file_name_out
        if 'setup' in self._section_name or 'deploy' in self._section_name:
            self._file_name_out = self._file_name_in
        else:
            filename = self._file_name_in.rsplit('.', 1)[0]
            extension = self._section_name_no_filter
            self._file_name_out = filename + '.' + extension

    def _update_context(self):
        """Updates Context with the name of files being manipulated in this job execution.
        """
        base_file_name = self._file_name_out.rsplit('.', 1)[0]

        Context().add_env_variable('$OF_COMPILE_IN', self._file_name_in)
        Context().add_env_variable('$OF_COMPILE_OUT', self._file_name_out)
        Context().add_env_variable('$OF_COMPILE_BASE', base_file_name)

    def _process_option(self, key, value):
        """Processes option like an environment or a filter variable.

        The return code of this method is either 0 or 1, and not negative since it is just a warning 
        and not an error worth stopping the program execution.

        Raises:
            SystemError: An error occurs if the input option (key and value pair) is not supported.

        Returns
            An integer, the return code of the method.
        """
        try:
            if key.startswith('$'):
                Context().add_env_variable(key, value)
                if key == '$OF_COMPILE_IN':
                    self._file_name_in = Context().env['OF_COMPILE_IN']
                elif key == '$OF_COMPILE_OUT':
                    self._file_name_out = Context().env['OF_COMPILE_OUT']
            elif key.startswith('?'):
                Context().add_filter(key, value)
            else:
                raise Warning()
        except Warning:
            Log().logger.warning('[' + self._section_name +
                                 '] Option not supported, skipping: ' + key)
        finally:
            return 0