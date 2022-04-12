#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Handle some of the test cases for the Source module.
"""

# Generic/Built-in modules
import os
import sys

# Third-party modules
import pytest

# Owned modules
from ....oftools_compile.Main import Main


class TestSource():
    """Test cases for the method _analyze.

    Fixtures:
        init_pwd

    Tests:
        test_default
        test_comma_separated_list
        test_text        
    """
    
    @staticmethod
    @pytest.fixture
    def init_pwd():
        """Specify the absolute path of the current test directory.
        """
        pwd = os.getcwd() + '/tests/unit/source/'
        return pwd