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


class TestProfileFilters(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_profile_filter_true
        test_profile_filter_false
        test_profile_filter_true_false
        test_profile_filter_true_false_same
        test_profile_filter_true_middle
    """

    @pytest.fixture
    def init_pwd(self):
        """
        """
        pwd = os.getcwd() + '/tests/unit/test_profile_filters/'
        return pwd

    def test_profile_filter_true(self, init_pwd):
        """Test with a profile where this is a filter variable being True.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'filter_true.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_filter_false(self, init_pwd):
        """Test with a profile where this is a filter variable being False.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'filter_false.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_filter_true_false(self, init_pwd):
        """Test with a profile where this is a filter variable being True then False.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'filter_true_false.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_filter_true_false_same(self, init_pwd):
        """Test with a profile where this is a filter variable being defined twice, one the filter is True, one the filter is False.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'filter_true_false_same.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_filter_true_middle(self, init_pwd):
        """Test with a profile where this is a filter variable being defined in the middle of the profile, and then being True.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'filter_true_middle.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0