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


class TestProcessTDL(object):
    """Test cases for the method _process_tdl, where the profile has both 'file' and 'tdl' options enabled.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_invalid_list
        test_multiple
        test_not_exist
        test_one
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
    @pytest.mark.skip(reason='Test not currently supported')
    def test_invalid_list(init_pwd, shared):
        """Test with multiple tdls specified, but the list delimiter is incorrect.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/tdl_invalid_list.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() != 0

    @staticmethod
    @pytest.mark.skip(reason='Test not currently supported')
    def test_multiple(init_pwd, shared):
        """Test with multiple tdls specified.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/tdl_multi.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    @pytest.mark.skip(reason='Test not currently supported')
    def test_not_exist(init_pwd, shared):
        """Test with one tdl specified, but which does not exist in OpenFrame.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/tdl_not_exist.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # OSError
        assert Main().run() == -1

    @staticmethod
    @pytest.mark.skip(reason='Test not currently supported')
    def test_one(init_pwd, shared):
        """Test with one tdl specified.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/tdl_one.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0
