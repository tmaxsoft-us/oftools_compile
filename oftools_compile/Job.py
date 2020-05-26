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


class Job(object):
    _section = None
    _profile = None

    def __init__(self, section, profile):
        self._section = section
        self._profile = profile

    def _add_filter(self, key, value, in_name):
        Log().get().debug('add_filter: [' + key + ',' + value + ']')

        result = False
        shell_cmd = ""
        try:
            filter_key = self._resolve_section_filter(section)
            shell_cmd = Context().get_filter_value(filter_key)
        except:
            return True

        shell_cmd = shell_cmd.replace("$OF_COMPILE_IN", in_name)
        Log().get().debug(os.getcwd())
        Log().get().info("run shell_cmd: " + shell_cmd)

        env = Context().get_env()
        proc = subprocess.Popen([shell_cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                env=env)
        out, err = proc.communicate()

        # grep returns 0 if line matches
        if proc.returncode == 0:
            result = True

        Context().add_filter(key, result)

    def _evaluate_filter(self, section, in_name):
        if "?" not in section:
            return True

        return Context().get_filter_value(section)

    def _resolve_base_name(self, in_name):
        return in_name.rsplit('.', 1)[0]

    def _resolve_section_base(self, section):

        index = section.find('?')
        if index > 0:
            section = section[:index]

        return section

    def _resolve_section_filter(self, section):

        index = section.find('?')
        if index > 0:
            section = section[index:]

        return section

    def get_section(self):
        return self._section