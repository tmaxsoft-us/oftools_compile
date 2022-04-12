#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Context module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestGetFilterFunction(object):
    """Test cases for the method get_filter_function.

    Fixtures:
        init_pwd
        shared

    Tests:
        test_used_before_defined
    """

    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path to the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/context/'
        return pwd

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    @pytest.mark.xfail
    def test_default(init_pwd, shared):
        """Test with a profile where the filter function is used before defined.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(
            ['--profile', init_pwd + 'profiles/used_before_defined.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(KeyError):
            Main().run()