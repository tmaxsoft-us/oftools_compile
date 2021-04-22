#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import subprocess

# Third-party modules

# Owned modules
from .Log import Log
from .Context import Context
from .Profile import Profile


class Job(object):
    _section = None
    _profile = None

    def __init__(self, section, profile):
        self._section = section
        self._profile = profile

        self._section_data = self._profile.data[section]

    def _add_filter(self, key, value):
        #Log().get().debug('add_filter: [' + key + ',' +
        #                  os.path.expandvars(value) + ']')

        result = False
        shell_cmd = os.path.expandvars(value)

        env = Context().env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()

        if b'' != out:
            Log().get().debug(err.decode(errors='ignore'))
        if b'' != err:
            Log().get().debug(out.decode(errors='ignore'))

        # grep returns 0 if line matches
        if proc.returncode == 0:
            result = True

        Context().add_filter_result(key, result)

    def _remove_extension_name(self, in_name):
        return in_name.rsplit('.', 1)[0]

    def _remove_filter_name(self, section):

        index = section.find('?')
        if index > 0:
            section = section[:index]

        return section

    def _resolve_filter_name(self, section):

        index = section.find('?')
        if index > 0:
            section = section[index:]

        return section

    @property
    def section(self):
        return self._section
