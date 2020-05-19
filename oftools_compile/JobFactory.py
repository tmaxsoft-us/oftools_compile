#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules

# Third-party modules

# Owned modules
from .DeployJob import DeployJob
from .CompileJob import CompileJob
from .SetupJob import SetupJob

from .Config.Profile import Profile


class JobFactory:
    _is_setup = False
    _is_compile = False
    _is_deploy = False

    def __init__(self, config):
        self._config = config
        return

    def create(self, section):
        if section is None:
            return None
        elif section == "setup":
            self._is_setup = True
            return SetupJob(self._config)
        elif section == "deploy":
            self._is_deploy = True
            return DeployJob(self._config)
        else:
            self._is_compile = True
            return CompileJob(section, self._config)

    def is_fine(self):
        if self._is_setup is False:
            print('setup section missing in profile')
        if self._is_compile is False:
            print('compile section missing in profile')
        if self._is_deploy is False:
            print('deploy section missing in profile')

        return self._is_setup and self._is_compile and self._is_deploy