#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of methods useful in any module.

This module gathers a set of methods that are useful in many other modules. When a method is widely 
used in different modules, a general version of it is created and can be found here.

Typical usage example:
  Utils().execute_shell_command(shell_command, env)
"""

# Generic/Built-in modules
import os
import subprocess

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
        execute_shell_command(shell_command, env): Separate method to execute shell command.
    """

    def execute_shell_command(self, shell_command, command_type, env):
        """Separate method to execute shell command.
        
        This method is dedicated to execute a shell command and it handles exceptions in case of 
        failure.

        Args:
            shell_command: A string, the actual shell command that needs to be executed.
            command_type: A string, the type of the command to execute. As of right now, it is 
                either init, compile, deploy, env_variable or filter.
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

        if Log().level == 'DEBUG':
            if return_code != 0 and command_type != 'filter':
                Log().logger.error(stdout)
                Log().logger.error(stderr)
                Log().logger.error('return code: ' + str(return_code))
            else:
                Log().logger.debug(stdout)
                Log().logger.debug(stderr)
                Log().logger.debug('return code: ' + str(return_code))
        elif return_code != 0 and command_type != 'filter':
            Log().logger.error(stdout)
            Log().logger.error(stderr)

        return stdout, stderr, return_code
