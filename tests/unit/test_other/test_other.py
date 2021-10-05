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


class TestOther(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_tag
        test_working_directory_already_exist
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_other/'
        return pwd

    def test_oftools_compile(self, init_pwd):
        """Test with the tag option.
        """
        sys.argv = [sys.argv[0]]

        with pytest.raises(SystemExit):
            Main().run()

    def test_tag(self, init_pwd):
        """Test with the tag option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])
        sys.argv.extend(['--tag', 'test'])

        assert Main().run() == 0

    def test_working_directory_already_exist(self, init_pwd):
        """Test where the working directory for the given program already exists, so we need to assign 
        a new timestamp.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])
        sys.argv.extend(['--profile', init_pwd + 'default.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0