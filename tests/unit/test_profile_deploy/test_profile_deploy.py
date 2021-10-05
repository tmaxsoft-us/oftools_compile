#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

# Generic/Built-in modules
import os
import shutil
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProfileDeploy(object):
    """

    Fixtures:
        init_pwd
    
    Tests:
        test_profile_deploy_file_new
        test_profile_deploy_file_same
        test_profile_deploy_dataset
        test_profile_deploy_region
        test_profile_deploy_tdl
    """

    @pytest.fixture
    def init_pwd(self):
        """
        """
        pwd = os.getcwd() + '/tests/unit/test_profile_deploy/'
        return pwd

    def test_profile_deploy_file_new(self, init_pwd):
        """Test with a profile where in the deploy section there is a file option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_file_new.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_deploy_file_same(self, init_pwd):
        """Test with a profile where in the deploy section the file option tries to copy a file that already exists.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_file_same.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        # shutil.SameFileError
        assert Main().run() == 0

    def test_profile_deploy_dataset(self, init_pwd):
        """Test with a profile where in the deploy section there are the options file and dataset.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_dataset.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    def test_profile_deploy_region(self, init_pwd):
        """Test with a profile where in the deploy section there are the options file and region.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_region.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0

    @pytest.mark.skip(reason='no way of currently testing this')
    def test_profile_deploy_tdl(self, init_pwd):
        """Test with a profile where in the deploy section there are the options file and tdl.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_tdl.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        assert Main().run() == 0