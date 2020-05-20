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
import os

# Third-party modules

# Owned modules


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Utils(metaclass=SingletonMeta):
    _env = None
    _init_env = None
    _total_time = 0

    def __init__(self):
        self._init_env = os.environ.copy()
        self._env = self._init_env
        return

    def set_env(self, env):
        self._env = env

    def get_env(self):
        return self._env

    def clear(self):
        self._env = self._init_env
