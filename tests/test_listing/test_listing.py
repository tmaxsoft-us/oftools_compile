#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys

from oftools_compile.Listing  import Listing

    #args = ["-p", "tests/test_listing/PROFILE1.txt", "-s", "tests/test_listing/add01.cob"]
def test_listing():
    print("\nRunning test_example...")
    source = "test/test_listing/PROFILE1.txt"
    profile = "tests/test_listing/add01.cob"
    listing = Listing(source, profile)
    pass

