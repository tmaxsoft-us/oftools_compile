#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""
# Generic/Built-in modules

# Third-party modules

# Owned modules

class Job(object):
    """
    """

    def __init__(self, section, profile):
        """
        """
        self._section = section
        self._profile = profile

        self._section_data = self._profile.data[section]

    @property
    def section(self):
        """
        """
        return self._section
