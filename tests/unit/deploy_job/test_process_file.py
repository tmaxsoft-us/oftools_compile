#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the DeployJob module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProcessFile(object):
    """Test cases for the method _process_file.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_new
        test_same
        test_fail
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path to the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/deploy_job/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_new(init_pwd, shared):
        """Test with a profile where in the deploy section there is a file option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/file_new.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_same(init_pwd, shared):
        """Test with a profile where in the deploy section the file option tries to copy a file that already exists.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/file_same.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # shutil.SameFileError
        assert Main().run() == 0

    @staticmethod
    def test_fail(init_pwd, shared):
        """Test with a profile where in the deploy section the file option tries to copy to an unauthorized location.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/file_fail.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # OSError: Permission denied
        assert Main().run() == -1