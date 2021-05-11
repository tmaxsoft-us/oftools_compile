#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log
from .Utils import Utils


class Profile():
    """

    Attributes:
        _data:
        _sections:
        _is_setup:
        _is_compile:
        _filter_variables:
        _env_variables:

    Methods:
        __init__():
        _analyze():
        _analyze_setup():
        _analyze_compile(section):
        _analyze_deploy():
        is_filter(section):
        evaluate_filter(section):
        remove_filter(section):
    """

    def __init__(self, path_to_profile):
        """
        """
        self._data = Utils().read_file(path_to_profile)
        self._sections = self._data.sections()

        self._is_setup = False
        self._is_compile = False
        self._is_deploy = False

        self._analyze()

    @property
    def data(self):
        """
        """
        return self._data

    @property
    def sections(self):
        """
        """
        return self._sections

    def _analyze(self):
        """
        """
        for section in self._sections:
            if section == None:
                #TODO Find proper implementation
                pass
            if section.startswith('setup'):
                self._is_setup = True
                self._analyze_setup()
            elif section.startswith('deploy'):
                self._is_deploy = True
                self._analyze_deploy()
            else:
                self._is_compile = True
                self._analyze_compile(section)

        if self._is_setup == False:
            Log().logger.critical('Missing setup section in the profile.')
            exit(-1)
        if self._is_compile == False:
            Log().logger.critical('Missing compile section in the profile.')
            exit(-1)

    def _analyze_setup(self):
        """
        """
        if self._data.has_option('setup', 'workdir') == True:
            root_workdir = self._data.get('setup', 'workdir')
            root_workdir = os.path.expandvars(root_workdir)
            if os.path.isdir(root_workdir) == True and os.access(root_workdir,
                                                            os.W_OK) == True:
                Context().root_workdir(root_workdir)
                # Create report directory if it does not already exist
                reportdir = os.path.join(root_workdir, 'report')
                if not os.path.isdir(reportdir):
                    os.mkdir(reportdir)
            else:
                Log().logger.critical('[setup] No write access on workdir = ' +
                                      root_workdir)
                exit(-1)
        else:
            Log().logger.critical(
                '[setup] Cannot find workdir parameter in the section.')
            exit(-1)

    def _analyze_compile(self, section):
        """
        """
        if self._data.has_option(section, 'option') == True:
            pass
        else:
            Log().logger.critical('[' + section + '] Missing "option" parameter.')
            exit(-1)        

    def _analyze_deploy(self):
        """
        """
        pass

    def has_filter(self, section):
        """
        """
        if 'setup' not in section and '?' in section:
            return True
        else:
            return False

    def evaluate_filter(self, value):
        """
        """
        env = Context().env()
        out, err, rc = Utils().execute_shell_command(value, env)

        #? What is it for?
        if out != b'':
            Log().logger.debug(err.decode(errors='ignore'))
        if err != b'':
            Log().logger.debug(out.decode(errors='ignore'))

        # grep command returns 0 if line matches
        if rc == 0:
            result = True
        else:
            result = False

        return result
