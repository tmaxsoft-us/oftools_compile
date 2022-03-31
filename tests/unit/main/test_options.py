#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Main module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestOptions(object):
    """Test cases for some of the command line options.

    Fixtures:
        shared

    Tests:
        test_help
        test_no_option
        test_tag
        test_version
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_help():
        """Test with the help option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--help')

        with pytest.raises(SystemExit):
            Main().run()

    @staticmethod
    def test_no_option():
        """Test with no option to see help message output.
        """
        sys.argv = [sys.argv[0]]

        with pytest.raises(SystemExit):
            Main().run()

    @staticmethod
    def test_tag(shared):
        """Test with the tag option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--tag', 'test'])

        assert Main().run() == 0

    @staticmethod
    def test_version():
        """Test with the version option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--version')

        with pytest.raises(SystemExit):
            Main().run()
