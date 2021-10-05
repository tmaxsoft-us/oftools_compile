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


class TestLogLevel(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_log_level_debug
        test_log_level_info
        test_log_level_warning
        test_log_level_error
        test_log_level_critical
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_log_level/'
        return pwd

    def test_log_level_debug(self, init_pwd):
        """Test with the log level option set to DEBUG.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_log_level_info(self, init_pwd):
        """Test with the log level option set to INFO.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'INFO'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_log_level_warning(self, init_pwd):
        """Test with the log level option set to WARNING.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'WARNING'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_log_level_error(self, init_pwd):
        """Test with the log level option set to ERROR.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'ERROR'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_log_level_critical(self, init_pwd):
        """Test with the log level option set to CRITICAL.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'CRITICAL'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0