#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the FileHandler module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestGetFiles(object):
    """Test cases for the method get_files.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_file_not_found_error
        test_directory_not_found_error
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
    def test_file_not_found_error(shared):
        """Test with a file that does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/FILENOTFOUND1.cbl'])

        with pytest.raises(FileNotFoundError):
            Main().run()
    
    @staticmethod
    @pytest.mark.xfail
    def test_directory_not_found_error(shared):
        """Test with a directory that does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/directory_not_found'])

        with pytest.raises(FileNotFoundError):
            Main().run()
