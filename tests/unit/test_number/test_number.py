#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os
import sys

# Third party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestNumber(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_number_profile_error
        test_number_source_error
        test_number_profile_reuse
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_number/'
        return pwd

    @pytest.mark.xfail
    def test_number_profile_error(self, init_pwd):
        """Test with two profiles and one source provided.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'number_1.prof'])
        sys.argv.extend(['--profile', init_pwd + 'number_2.prof'])
        sys.argv.extend(['--source', init_pwd + 'sample_1.cob'])

        with pytest.raises(SystemError):
            Main().run()

    @pytest.mark.xfail
    def test_number_source_error(self, init_pwd):
        """Test with one profile and two sources provided.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'number_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sample_1.cob'])
        sys.argv.extend(['--source', init_pwd + 'sample_2.cob'])

        with pytest.raises(SystemError):
            Main().run()

    def test_number_profile_reuse(self, init_pwd):
        """Test with one profile used twice.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'number_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sample_1.cob'])
        sys.argv.extend(['--profile', init_pwd + 'number_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sample_2.cob'])
        
        assert Main().run() == 0