#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestGrouping(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_grouping
        test_grouping_with_clear
    """

    @pytest.fixture
    def init_pwd(self):
        """
        """
        pwd = os.getcwd() + '/tests/unit/test_grouping/'
        return pwd

    def test_grouping(self, init_pwd):
        """Test with the grouping option enabled.
        #TODO Try to use temporary directory here, maybe?
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--grouping')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/'])

        assert Main().run() == 0

    def test_grouping_with_clear(self, init_pwd):
        """Test with the grouping option enabled, as well as the clear option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.append('--grouping')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/'])

        assert Main().run() == 0