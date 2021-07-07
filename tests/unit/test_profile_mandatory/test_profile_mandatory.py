#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProfileMandatory(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_profile_mandatory_option_empty_warning
        test_profile_mandatory_section_not_exist_warning
        test_profile_mandatory_section_with_filter_warning
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_profile_mandatory/'
        return pwd
    
    def test_profile_mandatory_option_empty_warning(self, init_pwd):
        """Test with a profile where a setup section with an empty mandatory option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'mandatory_option_empty.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        # Warning
        assert Main().run() == 0

    def test_profile_mandatory_section_not_exist_warning(self, init_pwd):
        """Test with a profile where a section specified in the mandatory list does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'mandatory_section_not_exist.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        # Warning
        assert Main().run() == 0

    def test_profile_mandatory_section_with_filter_warning(self, init_pwd):
        """Test with a profile where a section specified in the mandatory list contains a filter variable.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'mandatory_section_with_filter.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        # Warning
        assert Main().run() == 0