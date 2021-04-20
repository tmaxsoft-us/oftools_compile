#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of functions useful in any module.

This module gathers a set of functions that are useful in many other modules. When a 
function is widely used in different modules, a general version of it is created and 
can be found here.

  Typical usage example:

  utils = Utils()
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Utils(metaclass=SingletonMeta):
    """A class used to run several useful functions across all modules.

    Attributes:

    Methods:
    """
