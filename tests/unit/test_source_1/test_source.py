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


class TestSource():
    """

    Fixtures:
        init_pwd

    Tests:
        test_dot_file
        test_dot_dot_file
        test_dot_directory
        test_dot_dot_directory
        test_file_not_found_error_1
        test_file_not_found_error_2
    """
    @pytest.fixture
    def init_pwd(self):
        """
        """
        pwd = os.getcwd() + '/tests/unit/test_source_1/'
        return pwd

    def test_dot_file(self, init_pwd):
        """Test with '.' in the path of the source, source being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', './sample_1.cob'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    def test_dot_dot_file(self, init_pwd):
        """Test with '..' in the path of the source, source being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', '../test_source_2/sample_1.cob'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    def test_dot_directory(self, init_pwd):
        """Test with '.' in the path of the source, source being a directory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', './sources/'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    def test_dot_dot_directory(self, init_pwd):
        """Test with '..' in the path of the source, source being a directory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', '../test_source_2/'])

        current_pwd = os.getcwd()
        os.chdir(init_pwd)
        assert Main().run() == 0
        os.chdir(current_pwd)

    @pytest.mark.xfail
    def test_file_not_found_error_1(self, init_pwd):
        """Test with a file that does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'file_not_found.cob'])

        with pytest.raises(FileNotFoundError):
            Main().run()

    @pytest.mark.xfail
    def test_file_not_found_error_2(self, init_pwd):
        """Test with a directory that does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend('--source', init_pwd + 'directory_not_found/')

        with pytest.raises(FileNotFoundError):
            Main().run()

