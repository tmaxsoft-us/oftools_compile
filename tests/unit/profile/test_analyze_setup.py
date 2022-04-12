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


class TestAnalyzeSetup(object):
    """Test cases for the method _analyze_setup.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_working_directory_missing
        test_working_directory_empty
        test_not_a_directory
        test_no_write_access
        test_mandatory_empty
        test_mandatory_filter_warning
        test_mandatory_not_exist_warning
        test_mandatory_not_exist_filter_warning
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
    def test_working_directory_missing(init_pwd, shared):
        """Test with a profile missing the workdir option in the setup section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/workdir_missing.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(SystemError):
            Main().run()

    @staticmethod
    @pytest.mark.xfail
    def test_working_directory_empty(init_pwd, shared):
        """Test with a profile where the workdir option is empty.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/workdir_empty.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(ValueError):
            Main().run()

    @staticmethod
    @pytest.mark.xfail
    def test_not_a_directory(init_pwd, shared):
        """Test with the working directory specified being a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/not_a_directory.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(OSError):
            Main().run()

    @staticmethod
    @pytest.mark.xfail
    def test_no_write_access(init_pwd, shared):
        """Test with the user not having write access on the working directory specified.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/no_write_access.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(OSError):
            Main().run()

    @staticmethod
    def test_mandatory_empty(init_pwd, shared):
        """Test with a profile where the mandatory option is empty.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/mandatory_empty.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # ValueError
        assert Main().run() == 0

    @staticmethod
    def test_mandatory_filter_warning(init_pwd, shared):
        """Test with a profile where a section specified in the mandatory list contains a filter variable.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/mandatory_filter.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # Warning
        assert Main().run() == 0

    @staticmethod
    def test_mandatory_not_exist_warning(init_pwd, shared):
        """Test with a profile where a section specified in the mandatory list does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/mandatory_not_exist.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # Warning
        assert Main().run() == 0

    @staticmethod
    def test_mandatory_not_exist_filter_warning(init_pwd, shared):
        """Test with a profile where a section specified in the mandatory list does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend([
            '--profile', init_pwd + 'profiles/mandatory_not_exist_filter.prof'
        ])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # Warning
        assert Main().run() == 0