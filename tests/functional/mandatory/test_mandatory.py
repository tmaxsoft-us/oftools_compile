#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the option mandatory.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestMandatory(object):
    """Test cases for the mandatory profile option.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_all_sections_with_filters
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path to the current test directory.
        """
        pwd = os.getcwd() + '/tests/functional/mandatory/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_all_sections_with_filters(init_pwd, shared):
        """Test with a profile where all the section have filter and some are mandatory.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/all_sections_with_filters.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        assert Main().run() == 0