#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Main module.
"""

# Generic/Built-in modules
import os
import signal
import subprocess
import sys

# Third-party modules
import pytest

# Owned modules


class TestKeyboardInput(object):
    """Test cases for the KeyboardInterrupt exception.

    Fixtures:
        shared

    Tests:
        test_ctrl_c
        test_ctrl_backslash
    """

    @staticmethod
    @pytest.fixture
    def shared():
        """Specify the absolute path of the shared directory.
        """
        pwd = os.getcwd() + '/tests/shared/'
        return pwd

    @staticmethod
    def test_ctrl_c(shared):
        """Test with a Ctrl + C input to send the signal SIGINT and raise the KeyboardInterrupt exception to cancel the current compilation.
          """
        sys.argv = ['oftools_compile']
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        process = subprocess.Popen(sys.argv,
                                   universal_newlines=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        process.send_signal(signal.SIGINT)
        process.communicate()

        assert process.returncode == -2

    @staticmethod
    def test_ctrl_backslash(shared):
        """Test with a Ctrl + \\ input to send the signal SIGQUIT and fully abort the program execution.
          """
        sys.argv = ['oftools_compile']
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', shared + 'profiles/default_1.prof'])
        sys.argv.extend(['--source', shared + 'sources/SAMPLE1.cbl'])

        process = subprocess.Popen(sys.argv,
                                   universal_newlines=True,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        process.send_signal(signal.SIGQUIT)
        process.communicate()

        assert process.returncode == -3
