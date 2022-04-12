#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the different types of source.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestSource():
    """Test cases for the Source module.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_dot_file
        test_dot_dot_file
        test_dot_directory
        test_dot_dot_directory
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """
        """
        pwd = os.getcwd() + '/tests/functional/source_1/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_dot_file(init_pwd, shared):
        """Test with '.' in the path of the source, source being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', './SAMPLE1.cbl'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    @staticmethod
    def test_dot_dot_file(init_pwd, shared):
        """Test with '..' in the path of the source, source being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', '../source_2/SAMPLE1.cbl'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    @staticmethod
    def test_dot_directory(init_pwd, shared):
        """Test with '.' in the path of the source, source being a directory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', './sources/'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    @staticmethod
    def test_dot_dot_directory(init_pwd, shared):
        """Test with '..' in the path of the source, source being a directory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', '../source_2/'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)
