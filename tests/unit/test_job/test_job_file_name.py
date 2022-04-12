#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test regarding the Job module about the input file name.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestJob(object):
    """A class for all test cases related to special characters in the input file name.

        Fixtures:
            init_pwd

        Tests:
            test_dollar_sign
            test_number_sign
            test_at_sign
        """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Fixture to initialize the path to the test files.
            """
        pwd = os.getcwd() + '/tests/unit/test_job/'
        return pwd

    @staticmethod
    def test_dollar_sign(init_pwd):
        """Test with an input file starting with a $.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'asm.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/$sample.asm'])

        assert Main().run() == 0

    @staticmethod
    def test_number_sign(init_pwd):
        """Test with an input file starting with a #.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'asm.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/#sample.asm'])

        assert Main().run() == 0

    @staticmethod
    def test_at_sign(init_pwd):
        """Test with an input file starting with a @.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'asm.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/@sample.asm'])

        assert Main().run() == 0
