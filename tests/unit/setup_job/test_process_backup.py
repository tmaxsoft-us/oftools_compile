#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the SetupJob module.
"""

# Generic/Built-in modules
import glob
import os
import shutil
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProcessBackup(object):
    """Test cases for the method _process_backup.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_2_duplicates
        test_5_duplicates
        test_empty
        test_value_error
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/setup_job/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_2_duplicates(init_pwd, shared):
        """Test with the backup value set to 4, and 2 compilation being executed.
        """
        pattern = '/opt/tmaxapp/compile/SAMPLE1*'
        for item in glob.glob(pattern):
            if not os.path.isdir(item):
                continue
            shutil.rmtree(item)

        for _ in range(2):
            sys.argv = [sys.argv[0]]
            sys.argv.extend(['--log-level', 'DEBUG'])
            sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
            sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

            Main().run()

        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/backup.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_5_duplicates(init_pwd, shared):
        """Test with the backup value set to 4, and 5 compilation being executed.
        """
        pattern = '/opt/tmaxapp/compile/SAMPLE1*'
        for item in glob.glob(pattern):
            if not os.path.isdir(item):
                continue
            shutil.rmtree(item)

        for _ in range(5):
            sys.argv = [sys.argv[0]]
            sys.argv.extend(['--log-level', 'DEBUG'])
            sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
            sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

            Main().run()

        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/backup.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_empty(init_pwd, shared):
        """Test with a profile where the backup option is empty.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/backup_empty.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # ValueError
        assert Main().run() == 0

    @staticmethod
    @pytest.mark.xfail
    def test_value_error(init_pwd, shared):
        """Test with the backup value in the profile being a string and not an int, raising the ValueError exception.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/backup_value_error.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(ValueError):
            Main().run()
