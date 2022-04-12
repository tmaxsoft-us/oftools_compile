#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Grouping module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestGrouping(object):
    """Test cases for the whole class Grouping.

    Fixtures:
        shared

    Tests:
        test_grouping
        test_grouping_with_clear
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_grouping(shared):
        """Test with the grouping option enabled.
        #TODO Try to use temporary directory here, maybe?
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--grouping')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/'])

        assert Main().run() == 0

    @staticmethod
    def test_grouping_with_clear(shared):
        """Test with the grouping option enabled, as well as the clear option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.append('--grouping')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/'])

        assert Main().run() == 0