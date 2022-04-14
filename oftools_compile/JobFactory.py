#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to retrieve the parameters entered by the user and launch the corresponding job.

Typical usage example:
  job_factory = JobFactory(profile)
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .DeployJob import DeployJob
from .CompileJob import CompileJob
from .SetupJob import SetupJob


class JobFactory(object):
    """A class used to create all the jobs required with the given profile.

    Attributes:
        _profile {Profile}

    Methods:
        __init__(profile) -- Initializes the class with the _profile attribute.
        create(section_name) -- Creates the job according to the input parameter.
    """

    def __init__(self, profile):
        """Initializes the class with the _profile attribute.
        """
        self._profile = profile

    def create(self, section_name):
        """Creates the job according to the input parameter.

        Arguments:
            section_name {string} -- Name of the section in the profile.

        Returns:
            Job object -- Appropriate Job object depending on the input.
        """
        if section_name.startswith('setup'):
            return SetupJob(self._profile, section_name)
        elif section_name.startswith('deploy'):
            return DeployJob(self._profile, section_name)
        else:
            return CompileJob(self._profile, section_name)