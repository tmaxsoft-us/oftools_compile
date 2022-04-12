#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Job module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProcessOption(object):
    """Test cases for the method _process_option.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_unsupported_option
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path to the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/job_new/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_unsupported_option(init_pwd, shared):
        """Test with a profile where there is an unsupported option in one of the sections, that is going to be skipped.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/unsupported_option.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # Warning
        assert Main().run() == 0