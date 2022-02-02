#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module to do some testing related to the Profile module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProfile(object):
    """A class to test the correct behavior of the complete sections dictionary in the Profile 
    module.

    Fixtures:
        init_pwd

    Tests:
        test_2_programs
        test_3_programs
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_profile/'
        return pwd

    @staticmethod
    def test_2_programs(init_pwd):
        """Test with two different compilations in a row, one COBOL and then one Assembler program.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'cbl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample1.cbl'])
        sys.argv.extend(['--profile', init_pwd + 'jcl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.jcl'])

        assert Main().run() == 0

    @staticmethod
    def test_3_programs(init_pwd):
        """Test with three different compilations in a row, one COBOL, one Assembler, and then another COBOL program.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'cbl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample1.cbl'])
        sys.argv.extend(['--profile', init_pwd + 'jcl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.jcl'])
        sys.argv.extend(['--profile', init_pwd + 'cbl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample2.cbl'])

        assert Main().run() == 0
