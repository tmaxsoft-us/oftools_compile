#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the SetupJob module.
"""

# Generic/Built-in modules
import datetime
import glob
import os
import shutil
import sys
import time

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProcessHousekeeping(object):
    """Test cases for the method _process_housekeeping.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_30_days
        test_not_old_enough
        test_missing_backup
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
    def test_30_days(init_pwd, shared):
        """Test with housekeeping enabled to delete directories older than 30 days.
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

        working_directories = [
            d.path for d in os.scandir('/opt/tmaxapp/compile')
            if d.is_dir(follow_symlinks=True) and 'SAMPLE1' in d.name
        ]
        latest_directory = max(working_directories, key=os.path.getmtime)
        date = datetime.datetime.today() - datetime.timedelta(days=31)
        update = time.mktime(date.timetuple())
        os.utime(latest_directory, (update, update))

        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/housekeeping_30_days.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_not_old_enough(init_pwd, shared):
        """Test with no working directory old enough to be deleted.
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
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/housekeeping_30_days.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_missing_backup(init_pwd, shared):
        """Test with the housekeeping value in the profile used without specifying a backup option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend([
            '--profile', init_pwd + 'profiles/housekeeping_missing_backup.prof'
        ])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # ValueError
        assert Main().run() == -1

    @staticmethod
    def test_empty(init_pwd, shared):
        """Test with a profile where the housekeeping option is empty.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/housekeeping_empty.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_value_error(init_pwd, shared):
        """Test with the housekeeping value in the profile being a string and not an int, raising the ValueError exception.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/housekeeping_value_error.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == -1
