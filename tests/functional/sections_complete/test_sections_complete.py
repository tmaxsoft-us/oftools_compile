#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the _sections_complete dictionary.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestSectionsComplete(object):
    """Test cases for the dictionary _sections_complete in the Profile module.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_2_programs
        test_3_programs
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/functional/sections_complete/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_2_programs(init_pwd, shared):
        """Test with two different compilations in a row, one COBOL and then one JCL program.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/jcl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/SAMPLE.jcl'])

        assert Main().run() == 0

    @staticmethod
    def test_3_programs(init_pwd, shared):
        """Test with three different compilations in a row, one COBOL, one JCL, and then another COBOL program.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--profile', init_pwd + 'profiles/jcl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/SAMPLE.jcl'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE2.cbl'])

        assert Main().run() == 0
