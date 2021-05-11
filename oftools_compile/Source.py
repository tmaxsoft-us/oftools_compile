#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os

# Third-party modules

# Owned modules


class Source():
    """

    Attributes:
        _source_path:
        _files:

    Methods:
        __init__(source):
        _analyze(): Check whether source is a file or a folder and then create the source list.
    """

    def __init__(self, source_path):
        """
        """
        self._source_path = source_path
        self._files = []

        self._analyze()

    @property
    def files(self):
        """
        """
        return self._files

    def _analyze(self):
        """Check whether source is a file or a folder and then create the source list.
        """
        source = os.path.expandvars(self._source_path)

        if os.path.isfile(source):
            self._files = [source]

        elif os.path.isdir(source):
            for root, _, files in os.walk(source):
                if root.startswith('.'):
                    continue
                for name in files:
                    if name.startswith('.'):
                        continue
                    self._files.append(os.path.abspath(os.path.join(root, name)))

            # Sort the list alphabetically
            self._files.sort()

        return self._files