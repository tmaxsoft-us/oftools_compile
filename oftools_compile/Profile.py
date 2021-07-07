#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to handle all profile related tasks.

Typical usage example:
  profile = Profile(profile_path)
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules

# Owned modules
from .Context import Context
from .Log import Log
from .Utils import Utils


class Profile(object):
    """A class used to initialize the Profile object and analyze it.

    Attributes:
        _data: A ConfigParser object, the data extracted from the profile.
        _sections: A list, the name of the sections in the profile.
        _is_setup: A boolean, evaluates if there is a setup section in the profile.

    Methods:
        __init__(profile_path): Initializes the class with all the attributes.
        _analyze(): Analyzes the sections of the profile.
        _analyze_setup(): Analyzes the setup section of the profile.
        _analyze_compile(section): Analyzes any compile section of the profile.
        _analyze_deploy(): Analyzes the deploy section of the profile.
    """

    def __init__(self, profile_path):
        """Initializes the class with all the attributes.
        """
        self._data = Utils().read_file(profile_path)
        self._sections = self._data.sections()

        Log().logger.debug('Profile sections: ')
        Log().logger.debug(self._sections)

        self._is_setup = False

        self._analyze()

    @property
    def data(self):
        """Getter method for the attribute _data.
        """
        return self._data

    @property
    def sections(self):
        """Getter method for the attribute _sections.
        """
        return self._sections

    def _analyze(self):
        """Analyzes the sections of the profile.

        Initializes the dictionary complete_sections, makes sure that there is a setup section, and 
        handles potential errors.

        Raises:
            SystemError: An error occurs if the setup section is missing in the profile.
        """
        try:
            for section in self._sections:
                # Removing filter variables from the section name
                if '?' in section:
                    section_name_no_filter = section.split('?')[0]
                else:
                    section_name_no_filter = section
                # Sections dictionary initialization
                Context().complete_sections[section_name_no_filter] = False

                # Detailed analysis of the sections
                if section.startswith('setup'):
                    self._is_setup = True
                    self._analyze_setup()
                elif section.startswith('deploy'):
                    self._analyze_deploy()
                else:
                    self._analyze_compile(section)

            if self._is_setup is False:
                raise SystemError()
        except SystemError:
            Log().logger.critical('Missing section in the profile: setup')
            sys.exit(-1)

    def _analyze_setup(self):
        """Analyzes the setup section of the profile.

        Makes sure that the option 'workdir' is in the section, analyzes as well a potential 
        'mandatory' option.

        Raises:
            SystemError: An error occurs if the setup section does not contain a workdir option.
            SystemError: An error occurs if a section not existing in the profile is mentioned in the 
                mandatory list.
        """
        try:
            # Analyze working directory option
            if self._data.has_option('setup', 'workdir'):
                root_workdir = self._data.get('setup', 'workdir')
                root_workdir = os.path.expandvars(root_workdir)

                if os.path.isdir(root_workdir) and os.access(
                        root_workdir, os.W_OK):
                    # Save root working directory to Context
                    Context().root_workdir = root_workdir
                    # Create report directory if it does not already exist
                    reportdir = os.path.join(root_workdir, 'report')
                    if not os.path.isdir(reportdir):
                        os.mkdir(reportdir)
                else:
                    Log().logger.critical(
                        '[setup] Permission denied: No write access on workdir: '
                        + root_workdir)
                    sys.exit(-1)
            else:
                raise SystemError()
        except SystemError:
            Log().logger.critical(
                '[setup] Missing option in the section: workdir')
            sys.exit(-1)

        # Analyze mandatory option
        if self._data.has_option('setup', 'mandatory'):
            value = self._data.get('setup', 'mandatory')

            if value != '':
                # Split the mandatory sections in a list
                value = value.split(':')
                # Check that the mandatory section actually exist in the profile
                for section in value:
                    try:
                        if section in self._data.sections():
                            Context().add_mandatory_section(section)
                        else:
                            raise Warning()
                    except Warning:
                        Log().logger.warning(
                            '[setup] Mandatory section does not exist in current profile: Skipping section: '
                            + section)
                Log().logger.debug('[setup] Mandatory sections: ')
                Log().logger.debug(Context().mandatory_sections)
            else:
                Log().logger.warning(
                    '[setup] No mandatory section specified. Skipping option: mandatory'
                )

    def _analyze_compile(self, section):
        """Analyzes any compile section of the profile.

        Makes sure that the option 'args' or 'option' is in the section.

        Raises:
            SystemError: An error occurs if the given compile section does not contain an 'args' or 
                'option' option.
        """
        try:
            if self._data.has_option(section,
                                     'args') is False and self._data.has_option(
                                         section, 'option') is False:
                raise SystemError()
        except SystemError:
            Log().logger.critical('[' + section +
                                  '] Missing option in the section: args')
            sys.exit(-1)

    def _analyze_deploy(self):
        """Analyzes the deploy section of the profile.

        Makes sure that the option 'file' is in the section.

        Raises:
            SystemError: An error occurs if the deploy section does not contain a 'file' option.
        """
        try:
            if self._data.has_option('deploy', 'file') is False:
                raise SystemError()
        except SystemError:
            Log().logger.critical(
                '[deploy] Missing option in the section: file')
            sys.exit(-1)
