#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules

# Third-party modules

# Owned modules


class Profile:

    _section = None
    _options = None

    def __init__(self, section, options):
        self._section = section
        self._options = options
        return

    @property
    def section(self):
        return self._section

    @property
    def options(self):
        return self._options