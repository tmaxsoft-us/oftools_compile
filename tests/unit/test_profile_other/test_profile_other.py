#!/usr/bin/env python3
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


class TestProfileOther(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_profile_no_deploy_section
        test_profile_no_compile_section
        test_profile_compile_args_option
        test_profile_compile_option_option
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_profile_other/'
        return pwd

    def test_profile_no_deploy_section(self, init_pwd):
        """Test with a profile where there is no deploy section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'no_deploy.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_no_compile_section(self, init_pwd):
        """Test with a profile where there is no compile section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'no_compile.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_compile_args_option(self, init_pwd):
        """Test with a profile where there are both args and 'option' options in the compile sections.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'compile_args_option.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_compile_option_option(self, init_pwd):
        """Test with a profile where there is only the 'option' option in the compile sections.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'compile_option.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0