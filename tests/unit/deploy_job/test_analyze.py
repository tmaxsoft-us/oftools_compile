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


class TestAnalyze(object):
    """Test cases for the method _analyze.

    Fixtures:
        init_pwd
        shared
    
    Tests:
        test_compile_not_complete
        test_deploy_only
        test_filter_false
        test_filter_true
        test_section_complete
        test_section_mandatory
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
    def test_compile_not_complete(init_pwd, shared):
        """Test with no complete compile section found to run the deploy section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/compile_not_complete.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == -1

    @staticmethod
    def test_deploy_only(init_pwd, shared):
        """Test with no compile section found, so deploy section only.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/deploy_only.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_filter_false(init_pwd, shared):
        """Test with the deploy section with a filter being false.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/filter_false.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_filter_true(init_pwd, shared):
        """Test with the deploy section with a filter being true.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/filter_true.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_section_complete(init_pwd, shared):
        """Test with two deploy sections, to trigger the already complete case.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/section_complete.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0

    @staticmethod
    def test_section_mandatory(init_pwd, shared):
        """Test with the deploy section set as mandatory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/section_mandatory.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0
