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

    Methods:
    """

    def __init__(self, source):
        """
        """
        self._files = self._source_analysis(source)

    @property
    def files(self):
        """
        """
        return self._files

    def _source_analysis(self, source):
        """Check whether source is a file or a folder and then create the source list.
        """
        files = []
        directory = os.path.expandvars(source)

        if os.path.isdir(directory):
            for root, _, files in os.walk(directory):
                if root.startswith('.'):
                    continue
                for name in files:
                    if name.startswith('.'):
                        continue
                    files.append(os.path.abspath(os.path.join(root, name)))
        else:
            files = [source]

        # Sort the list alphabetically
        files.sort()

        return files