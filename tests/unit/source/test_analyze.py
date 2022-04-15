#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Source module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestAnalyze(object):
    """Test cases for the method _analyze.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_default_file
        test_default_skip
        test_default_directory
        test_colon_separated_list_file
        test_colon_separated_list_skip
        test_colon_separated_list_directory
        test_semicolon_separated_list_fail
        test_text_file
        test_text_skip
        test_text_directory
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/source/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_default_file(shared):
        """Test with the default source, here being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_default_skip(shared):
        """Test with the skip option and the default source, here being a missing file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SKIP.cbl'])
        sys.argv.append('--skip')

        assert Main().run() == 0

    @staticmethod
    def test_default_directory(shared):
        """Test with the default source, here being a directory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/'])

        assert Main().run() == 0

    @staticmethod
    def test_colon_separated_list_file(shared):
        """Test with a list of files as a source.
        """
        sources = shared + 'sources/SAMPLE1.cbl:' + shared + 'sources/SAMPLE2.cbl'

        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', sources])

        assert Main().run() == 0

    @staticmethod
    def test_colon_separated_list_skip(shared):
        """Test with a list of files as a source and the skip option.
        """
        sources = shared + 'sources/SAMPLE1.cbl:' + shared + 'sources/SKIP.cbl'

        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', sources])
        sys.argv.append('--skip')

        assert Main().run() == 0

    @staticmethod
    def test_colon_separated_list_directory(shared):
        """Test with a list of directories as a source.
        """
        sources = shared + 'sources/:' + shared + 'sources/'

        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', sources])

        assert Main().run() == 0

    @staticmethod
    @pytest.mark.xfail
    def test_semicolon_separated_list_fail(shared):
        """Test with a list of files as a source, but using the wrong delimiter.
        """
        sources = shared + 'sources/SAMPLE1.cbl;' + shared + 'sources/SAMPLE2.cbl'

        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', sources])

        with pytest.raises(FileNotFoundError):
            Main().run()

    @staticmethod
    def test_text_file(init_pwd, shared):
        """Test with a text file listing files as a source.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/files.txt'])

        assert Main().run() == 0

    @staticmethod
    def test_text_skip(init_pwd, shared):
        """Test with a text file listing files as a source, and the skip option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/skip.txt'])
        sys.argv.append('--skip')

        assert Main().run() == 0

    @staticmethod
    def test_text_directory(init_pwd, shared):
        """Test with a text file listing directories as a source.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/directories.txt'])

        assert Main().run() == 0
