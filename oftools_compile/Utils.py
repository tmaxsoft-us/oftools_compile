#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of methods useful in any module.

This module gathers a set of methods that are useful in many other modules. When a method is widely 
used in different modules, a general version of it is created and can be found here.

Typical usage example:
  Utils().read_file(profile_path)
  Utils().execute_shell_command(shell_command, env)
"""

# Generic/Built-in modules
import configparser
import collections
import os
import subprocess
import sys

# Third-party modules

# Owned modules
from .Log import Log


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Utils(object, metaclass=SingletonMeta):
    """A class used to run several useful functions across all modules.

    Methods:
        read_file(path_to_file):
        execute_shell_command(shell_command, env)
    """

    def read_file(self, path_to_file):
        """Open and read the input file.

        Supports following extensions:
            - configuration: conf, cfg, prof
            - text: log, tip, txt

        Args:
            path_to_file: A string, absolute path to the file.

        Returns: 
            A parsed file, the type depends on the extension of the processed file.

        Raises:
            FileNotFoundError: An error occurs if the file does not exist or is not found.
            IsADirectoryError: An error occurs if a directory is specified instead of a file.
            PermissionError: An error occurs if the user running the program does not have the required 
                permissions to access the input file.
            SystemExit: An error occurs of the file is empty.
            TypeError: An error occurs if the file extension is not supported.

            MissingSectionHeaderError: An error occurs if the config file specified does not contain 
                any section.
            DuplicateSectionError: An error occurs if there are two sections with the same name in the 
                config file specified.
            DuplicateOptionError: An error occurs if there is a duplicate option in one of the sections 
                of the config file specified.
        """
        try:
            path_to_file = os.path.expandvars(path_to_file)
            # Check on file size
            if os.stat(path_to_file).st_size <= 0:
                raise SystemExit()

            if os.path.isfile(path_to_file):
                with open(path_to_file, mode='r') as fd:
                    extension = path_to_file.rsplit('.', 1)[1]

                    if extension in ('conf', 'cfg', 'prof'):
                        file = configparser.ConfigParser(
                            dict_type=collections.OrderedDict)
                        file.optionxform = str
                        file.read(path_to_file)
                    elif extension in ('log', 'tip', 'txt'):
                        file = fd.read()
                    else:
                        raise TypeError()
            elif os.path.isdir(path_to_file):
                raise IsADirectoryError()
            else:
                raise FileNotFoundError()

        except FileNotFoundError:
            Log().logger.critical(
                'FileNotFoundError: No such file or directory: ' + path_to_file)
            sys.exit(-1)
        except IsADirectoryError:
            Log().logger.critical('IsADirectoryError: Is a directory: ' +
                                  path_to_file)
            sys.exit(-1)
        except PermissionError:
            Log().logger.critical('PermissionError: Permission denied: ' +
                                  path_to_file)
            sys.exit(-1)
        except SystemExit:
            Log().logger.critical('EmptyError: File empty: ' + path_to_file)
            sys.exit(-1)
        except TypeError:
            Log().logger.critical('TypeError: Unsupported file extension: ' +
                                  path_to_file)
            sys.exit(-1)
        except configparser.MissingSectionHeaderError as e:
            Log().logger.critical('MissingSectionHeaderError: ' + str(e))
            sys.exit(-1)
        except configparser.DuplicateSectionError as e:
            Log().logger.critical('DuplicateSectionError: ' + str(e))
            sys.exit(-1)
        except configparser.DuplicateOptionError as e:
            Log().logger.critical('DuplicateOptionError: ' + str(e))
            sys.exit(-1)
        else:
            return file

    def execute_shell_command(self, shell_command, env):
        """Separate method to execute shell command.
        
        This method is dedicated to execute a shell command and it handles exceptions in case of 
        failure.

        Args:
            shell_command: A string, the actual shell command that needs to be executed.
            env: A dictionary, all the environment variables currently in the shell environment.

        Returns:
            A tuple, which is the stdout, stderr, and return code of the shell command.

        Raises:
            UnicodeDecodeError: An error occurred if decoding the shell command result failed 
                with utf-8. Use latin-1 instead.
        """
        try:
            shell_command = os.path.expandvars(shell_command)
            proc = subprocess.run(shell_command,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  env=env)
            stdout = proc.stdout.decode('utf_8')
            stderr = proc.stderr.decode('utf_8')
            return_code = proc.returncode
        except UnicodeDecodeError:
            stdout = proc.stdout.decode('latin_1')
            stderr = proc.stderr.decode('latin_1')
            return_code = proc.returncode
        except:
            stdout = None
            stderr = None
            return_code = -1
            return stdout, stderr, return_code

        if return_code < 0 and Log().level == 'DEBUG':
            print(stdout)
            print('\n')
            print(stderr)

        return stdout, stderr, return_code
