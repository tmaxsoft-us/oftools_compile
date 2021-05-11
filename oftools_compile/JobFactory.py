#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module retrieves the parameters entered by the user and launches the corresponding job.

  Typical usage example:

  job_factory = JobFactory(profile)
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .DeployJob import DeployJob
from .CompileJob import CompileJob
from .SetupJob import SetupJob


class JobFactory:
    """A class used to ...

    Attributes:
        _profile: ...

    Methods:
        __init__(): Initializes the _profile attribute.
        create(): Create the job according to the section parameter.
    """

    def __init__(self, profile):
        """Initializes the _profile attribute.
        """
        self._profile = profile

    def create(self, section_name):
        """Create the job according to the section parameter.

        Args:
            section: A string, the name of the section in the profile.

        Returns:
            Return the appropriate job.
        """
        if section_name.startswith('setup'):
            return SetupJob(section_name, self._profile)
        elif section_name.startswith('deploy'):
            return DeployJob(section_name, self._profile)
        else:
            return CompileJob(section_name, self._profile)
