#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Main module.
"""

# Generic/Built-in modules
import os
import sys

# Third party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestNumber(object):
    """Test cases for the number of inputs.

    Fixtures:
        shared

    Tests:
        test_profile_error
        test_profile_reuse
        test_source_error
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    @pytest.mark.xfail
    def test_profile_error(shared):
        """Test with two profiles and one source provided.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--profile', shared + 'profiles/default_2.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(SystemError):
            Main().run()

    @staticmethod
    def test_profile_reuse(shared):
        """Test with one profile used twice.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared+ 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE2.cbl'])

        assert Main().run() == 0

    @staticmethod
    @pytest.mark.xfail
    def test_source_error(shared):
        """Test with one profile and two sources provided.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE2.cbl'])

        with pytest.raises(SystemError):
            Main().run()