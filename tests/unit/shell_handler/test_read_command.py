#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the ShellHandler module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestReadCommand(object):
    """Test cases for the method read_command.
    
    Fixtures:
        shared

    Tests:
        test_unicode_decode_error
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    @pytest.mark.xfail
    @pytest.mark.skip(reason='Test not currently supported')
    def test_unicode_decode_error(shared):
        """Test with...
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        with pytest.raises(UnicodeDecodeError):
            Main().run()
