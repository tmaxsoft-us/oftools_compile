#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the SetupJob module.
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
        test_section_complete
        test_section_mandatory
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
    def test_section_complete(init_pwd, shared):
        """Test with two setup sections, to trigger the already complete case.
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
        """Test with the setup section set as mandatory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/section_mandatory.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0
