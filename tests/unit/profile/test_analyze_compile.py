#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Profile module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestAnalyzeCompile(object):
    """Test cases for the method _analyze_compile.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_args_missing
        test_args_empty
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/profile/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    @pytest.mark.xfail
    def test_args_missing(init_pwd, shared):
        """Test with a profile where the args option is missing in one of the compile sections.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/args_missing.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(SystemError):
            Main().run()

    @staticmethod
    @pytest.mark.xfail
    def test_args_empty(init_pwd, shared):
        """Test with a profile where the args option is empty in one of the compile sections.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/args_empty.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(ValueError):
            Main().run()