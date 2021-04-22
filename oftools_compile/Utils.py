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
import configparser
import collections
import sys
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
    """A class used to run several useful functions across all modules.

    Attributes:

    Methods:
    """


    def read_file(self, path_to_file):
        """Open and read the input file.

        Supports following extensions:
            - configuration: conf, cfg, prof
            - text: log, tip, txt

        Args:
            path_to_file: A string, absolute path to the file.

        Returns: A parsed file, the type depends on the extension of the processed file.

        Raises:
            FileTypeError: An error occurs if the file extension is not supported.
            FileNotFoundError: An error occurs if the file does not exist or is not found.
            PermissionError: An error occurs if the user running the program does not have the 
                required permissions to access the input file.
        """
        try:
            path_to_file = os.path.expandvars(path_to_file)
            with open(path_to_file, mode='r') as fd:
                extension = path_to_file.split('.')[-1]
                if extension in ('conf', 'cfg', 'prof'):
                    file = configparser.ConfigParser(dict_type=collections.OrderedDict)
                    file.optionxform = str
                    file.read(path_to_file)
                elif extension in ('log', 'tip', 'txt'):
                    file = fd.read()
                else:
                    print('FileTypeError: ' + path_to_file +
                          ': unsupported file extension.')
        except FileNotFoundError:
            print('FileNotFoundError: ' + path_to_file +
                  ': No such file or directory.')
            sys.exit(2)
        except PermissionError:
            print('PermissionError: ' + path_to_file + ': Permission denied.')
            sys.exit(3)
        else:
            return file
