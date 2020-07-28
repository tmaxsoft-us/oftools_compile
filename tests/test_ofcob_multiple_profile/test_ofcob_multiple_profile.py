#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import sys

from oftools_compile.Main import Main


#args = ["-p", "tests/test_listing/PROFILE1.txt", "-s", "tests/test_listing/add01.cob"]
def test_ofcob_multiple_profile():
    pwd = os.getcwd() + '/tests/test_ofcob_multiple_profile'
    sys.argv = [sys.argv[0]]
    sys.argv.append('-p')
    sys.argv.append(pwd + '/profile/ok.prof')
    sys.argv.append('-s')
    sys.argv.append(pwd + '/source')
    sys.argv.append('-p')
    sys.argv.append(pwd + '/profile/ok2.prof')
    sys.argv.append('-s')
    sys.argv.append(pwd + '/source2')
    sys.argv.append('-r')
    sys.argv.append('-l')
    sys.argv.append('DEBUG')

    return Main().run()