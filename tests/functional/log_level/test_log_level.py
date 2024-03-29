#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the log level.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestLogLevel(object):
    """Test cases for the different possibilities in terms of log level.

    Fixtures:
        shared

    Tests:
        test_debug
        test_info
        test_warning
        test_error
        test_critical
    """
    
    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_debug(shared):
        """Test with the log level option set to DEBUG.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_info(shared):
        """Test with the log level option set to INFO.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'INFO'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_warning(shared):
        """Test with the log level option set to WARNING.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'WARNING'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_error(shared):
        """Test with the log level option set to ERROR.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'ERROR'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_critical(shared):
        """Test with the log level option set to CRITICAL.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'CRITICAL'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0