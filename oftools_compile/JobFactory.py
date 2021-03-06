#!/usr/bin/python3
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
        _profile: A dictionary, the data extracted from the Profile object.

    Methods:
        __init__(profile): Initializes the class with the _profile attribute.
        create(section_name): Creates the job according to the input parameter.
    """

    def __init__(self, profile):
        """Initializes the class with the _profile attribute.
        """
        self._profile = profile.data

    def create(self, section_name):
        """Creates the job according to the input parameter.

        Args:
            section_name: A string, the name of the section in the profile.

        Returns:
            A Job object, the appropriate one depending on the input.
        """
        if section_name.startswith('setup'):
            return SetupJob(section_name, self._profile)
        elif section_name.startswith('deploy'):
            return DeployJob(section_name, self._profile)
        else:
            return CompileJob(section_name, self._profile)