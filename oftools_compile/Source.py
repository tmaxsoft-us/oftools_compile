#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle all source related tasks.

Typical usage example:
  source = Source(source_path)
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules

# Owned modules
from .Log import Log


class Source(object):
    """A class used to initialize the source and analyze it, to see if it a file or a directory.

    Attributes:
        _source_path: A string, the absolute path of the source.
        _file_paths: A list, all the files found in the source provided.

    Methods:
        __init__(source_path): Initializes the class with all the attributes.
        _analyze(): Creates the source list based on the input.
    """

    def __init__(self, source_path):
        """Initializes the class with all the attributes.
        """
        self._source_path = source_path
        self._file_paths = []

        self._analyze()

    @property
    def file_paths(self):
        """Getter method for the attribute _file_paths.
        """
        return self._file_paths

    def _analyze(self):
        """Creates the source list based on the input.

        It checks whether source is a file or a folder and then creates the source list.

        Raises:
            FileNotFoundError: An error occurs if the program does not find the given source.
        """
        source = os.path.expandvars(self._source_path)

        #TODO Supports a list or a text file as source input

        try:
            if os.path.exists(os.path.expandvars(source)) is False:
                raise FileNotFoundError()
        except FileNotFoundError:
            Log().logger.critical(
                'FileNotFoundError: No such file or directory: ' + source)
            sys.exit(-1)

        if os.path.isfile(source):
            self._file_paths = [os.path.abspath(source)]

        elif os.path.isdir(source):
            self._file_paths = [
                os.path.abspath(os.path.join(root, filename))
                for root, _, files in os.walk(source)
                for filename in files
                if not filename.startswith('.')
            ]
            # Sort the list alphabetically
            self._file_paths.sort()

        Log().logger.debug('Number of source files being compiled: ' +
                           str(len(self._file_paths)))
