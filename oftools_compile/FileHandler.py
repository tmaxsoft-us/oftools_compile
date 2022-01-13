#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of methods useful in any module.

This module gathers a set of methods that are useful in many other modules. When a method is widely 
used in different modules, a general version of it is created and can be found here.

Typical usage example:
  FileHandler().read_file(path)
"""

# Generic/Built-in modules
import configparser
import collections
import os
import shutil
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


class FileHandler(object, metaclass=SingletonMeta):
    """A class used to run several useful functions across all modules.

    Methods:
        read_file(path) -- Open and read a file.
        get_duplicates(path, pattern) -- Get duplicate files and folders in given path.
        get_creation_times(path) -- Get creation time of the input path(s).
        delete_directory(path) -- Delete an entire directory tree, whether it is empty or not.
    """

    def read_file(self, path):
        """Open and read the input file.

        It saves the file's content in a variable.

        Supports following extensions:
            - configuration: conf, cfg, prof
            - text: log, tip, txt

        Arguments:
            path {string} -- The absolute path to the file.

        Returns:
            A parsed file, the type depends on the extension of the processed file.

        Raises:
            FileNotFoundError: An error occurs if the file does not exist or is not found.
            IsADirectoryError: An error occurs if a directory is specified instead of a file.
            PermissionError: An error occurs if the user running the program does not have the 
            required permissions to access the input file.
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
            path = os.path.expandvars(path)
            # Check on file size
            if os.stat(path).st_size <= 0:
                raise SystemError()

            if os.path.isfile(path):
                with open(path, mode='r') as fd:
                    extension = path.rsplit('.', 1)[1]

                    if extension in ('conf', 'cfg', 'prof'):
                        file = configparser.ConfigParser(
                            dict_type=collections.OrderedDict)
                        file.optionxform = str
                        file.read(path)
                    elif extension in ('log', 'tip', 'txt'):
                        file = fd.read()
                    else:
                        raise TypeError()
            elif os.path.isdir(path):
                raise IsADirectoryError()
            else:
                raise FileNotFoundError()

        except FileNotFoundError:
            Log().logger.critical(
                'FileNotFoundError: No such file or directory: ' + path)
            sys.exit(-1)
        except IsADirectoryError:
            Log().logger.critical('IsADirectoryError: Is a directory: ' + path)
            sys.exit(-1)
        except PermissionError:
            Log().logger.critical('PermissionError: Permission denied: ' + path)
            sys.exit(-1)
        except SystemError:
            Log().logger.critical('EmptyError: File empty: ' + path)
            sys.exit(-1)
        except TypeError:
            Log().logger.critical('TypeError: Unsupported file extension: ' +
                                  path)
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

    def get_duplicates(self, path, pattern):
        """Get duplicate files and folders in the given path.

            Arguments:
                path {string} -- The absolute path to the directory.
                pattern {string} -- The string to identify duplicates.

            Returns:
                tuple -- A tuple with two lists, one for duplicate files and one for duplicate directories.
            
            Raises:
                NotADirectoryError -- An error occurs if the input path is not a directory.
                FileNotFoundError -- An error occurs if the directory does not exist or is not found.
                PermissionError -- An error occurs if the user running the program does not have the required permissions to access the input directory.
                OSError -- An exception is raised if an error didn't already raised one of the previous exceptions.
            """
        duplicate_files = []
        duplicate_directories = []

        try:
            if os.path.isdir(path):
                for element in os.scandir(path):
                    if element.is_file(
                            follow_symlinks=True) and pattern in element.name:
                        duplicate_files.append(element.path)
                    elif element.is_dir(
                            follow_symlinks=True) and pattern in element.name:
                        duplicate_directories.append(element.path)
            else:
                raise NotADirectoryError()

        except NotADirectoryError:
            Log().logger.error('NotADirectoryError: Is not a directory: ' +
                               path)
        except FileNotFoundError:
            Log().logger.error(
                'FileNotFoundError: No such file or directory: ' + path)
        except PermissionError:
            Log().logger.error('PermissionError: Permission denied: ' + path)
        except OSError as e:
            Log().logger.error('OSError: ' + str(e))

        return duplicate_files, duplicate_directories

    def get_creation_times(self, path):
        """Get creation time of the input path(s).

            Arguments:
                path {string or list} - One or several absolute path(s) to  files or directories.

            Returns:
                string or list -- The creation time(s) of the input path(s).
            """
        if isinstance(path, str):
            creation_time = os.path.getctime(path)
            return creation_time

        elif isinstance(path, list):
            paths = path
            creation_times = []

            for element in paths:
                creation_time = os.path.getctime(element)
                creation_times.append(creation_time)

            return creation_times

    def delete_directory(self, path):
        """Delete an entire directory tree, whether it is empty or not.

            Arguments:
                path {string} -- The absolute path to the directory.

            Returns:
                integer -- The return code of the method.

            Raises:
                NotADirectoryError -- An error occurs if the input path is not a directory.
                FileNotFoundError -- An error occurs if the directory does not exist or is not found.
                PermissionError -- An error occurs if the user running the program does not have the required permissions to access the input directory.
                OSError -- An exception is raised if an error didn't already raised one of the previous exceptions.
            """
        try:
            rc = 0
            path = os.path.expandvars(path)

            if os.path.isdir(path):

                # Check if directory is empty
                if len(os.listdir(path)) == 0:
                    Log().logger.debug('Directory empty: ' + path)
                    os.rmdir(path)
                else:
                    # Check on directory size
                    size = sum(
                        os.path.getsize(element)
                        for element in os.scandir(path)
                        if element.is_file(follow_symlinks=True))
                    if size == 0:
                        Log().logger.debug('Size of directory equal to 0: ' +
                                           path)

                    shutil.rmtree(path, ignore_errors=False)

                Log().logger.debug('Directory successfully removed: ' + path)
            else:
                raise NotADirectoryError()

        except NotADirectoryError:
            Log().logger.error('NotADirectoryError: Is not a directory: ' +
                               path)
            rc = -1
        except FileNotFoundError:
            Log().logger.error(
                'FileNotFoundError: No such file or directory: ' + path)
            rc = -1
        except PermissionError:
            Log().logger.error('PermissionError: Permission denied: ' + path)
            rc = -1
        except OSError as e:
            Log().logger.error('OSError: ' + str(e))
            rc = -1

        return rc
