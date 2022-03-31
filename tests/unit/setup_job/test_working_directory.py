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


class TestWorkingDirectory(object):
    """Test cases for the method _init_working_directory.

    Fixtures:
        shared

    Tests:
        test_already_exist
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_already_exist(shared):
        """Test where the working directory for the given program already exists, so a new timestamp needs to be assigned.
            """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        # FileExistsError
        assert Main().run() == 0