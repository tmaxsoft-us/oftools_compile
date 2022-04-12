#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to handle all source related tasks.

Typical usage example:
  source = Source(source_path)
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .enums.LogEnum import LogMessage
from .handlers.FileHandler import FileHandler
from .Log import Log


class Source(object):
    """A class used to initialize the source and analyze it, to see if this is a file or a directory.

    Attributes:
        _source_path {string} -- Absolute path of the source.
        _file_paths {list[string]} - List of files found in the source provided.

    Methods:
        __init__(source_path) -- Initializes the class with all the attributes.
        _analyze() -- Creates the source list based on the input.
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

        Returns:
            integer -- Return code of the method.
        """
        #TODO Supports a list or a text file as source input

        if FileHandler().check_path_exists(self._source_path):
            self._file_paths = FileHandler().get_files(self._source_path)
            Log().logger.debug(LogMessage.SOURCE_COUNT.value %
                               len(self._file_paths))
            rc = 0
        else:
            Log().logger.info(LogMessage.SOURCE_SKIP.value)
            rc = 1

        return rc
