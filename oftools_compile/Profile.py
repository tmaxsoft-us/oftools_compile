#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context

class Profile():
    """

    Attributes:

    Methods:
        evaluate_filter(key):
    """

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