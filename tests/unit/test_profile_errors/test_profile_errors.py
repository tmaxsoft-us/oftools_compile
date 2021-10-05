#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test suite for all the profile
#TODO pytest-benchmark
https://pytest-benchmark.readthedocs.io/en/latest/
#TODO bandit for security check on the application

#TODO Create a test where the order of the sections in the profile is not correct
"""

# Generic/Built-in modules
import configparser
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestProfileErrors(object):
    """

    Fixtures:
        init_pwd

    Tests:
        test_profile_type_error_1
        test_profile_type_error_2
        test_profile_index_error
        test_profile_file_not_found_error
        test_profile_is_a_directory_error
        test_profile_empty_error
        test_profile_missing_section_header_error
        test_profile_duplicate_section_error
        test_profile_missing_setup_error
        test_profile_setup_missing_workdir_error
        test_profile_compile_missing_args_error
        test_profile_deploy_missing_file_error
        test_profile_unsupported_option_error
    """

    @pytest.fixture
    def init_pwd(self):
        """Pytest fixture to specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/test_profile_errors/'
        return pwd

    @pytest.mark.xfail
    def test_profile_type_error_1(self, init_pwd):
        """Test with a file that does not have a .prof extension.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'extension_error_1.txt'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(TypeError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_type_error_2(self, init_pwd):
        """Test with a file that does not have a .prof extension.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'extension_error_2.err'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(TypeError):
            Main().run()
    
    @pytest.mark.xfail
    def test_profile_index_error(self, init_pwd):
        """Test with a directory instead of a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'is_a_directory/'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(IndexError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_file_not_found_error(self, init_pwd):
        """Test with a profile that does not exist.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'file_not_found.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(FileNotFoundError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_is_a_directory_error(self, init_pwd):
        """Test with a directory instead of a file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'is_a_directory.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(IsADirectoryError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_empty_error(self, init_pwd):
        """Test with a empty file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'empty.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(SystemError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_missing_section_header_error(self, init_pwd):
        """Test with a profile where there is no section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'no_section.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(configparser.MissingSectionHeaderError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_duplicate_section_error(self, init_pwd):
        """Test with a profile where there are two sections with the same name.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'duplicate_section.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(configparser.DuplicateSectionError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_missing_setup_error(self, init_pwd):
        """Test with a profile where there is no setup section.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'no_setup.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(SystemError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_setup_missing_workdir_error(self, init_pwd):
        """Test with a profile where there is a setup section without the workdir option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'setup_missing_workdir.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(SystemError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_compile_missing_args_error(self, init_pwd):
        """Test with a profile where there is a compile section without the option args or option.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'compile_missing_args.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(SystemError):
            Main().run()

    @pytest.mark.xfail
    def test_profile_deploy_missing_file_error(self, init_pwd):
        """Test with a profile where there is a deploy section without the option file.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'deploy_missing_file.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        with pytest.raises(SystemError):
            Main().run()

    def test_profile_unsupported_option_error(self, init_pwd):
        """Test with a profile where there is an unsupported option in one of the sections, that is going to be skipped.
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--clear')
        sys.argv.extend(['--log-level', 'DEBUG'])
        sys.argv.extend(['--profile', init_pwd + 'unsupported_option.prof'])
        sys.argv.extend(['--source', init_pwd + 'sources/sample.cob'])

        # Warning
        assert Main().run() == 0