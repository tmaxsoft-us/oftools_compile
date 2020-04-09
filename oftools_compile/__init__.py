import os
import sys
import getopt
from .Listing import Listing
from .Parser import Parser


def run_oftools_compile(argv):
    source_name = ""
    profile_name = ""
    try:
        opts, args = getopt.getopt(argv, "hp:s:",
                                   ["profile_name=", "source_name="])
    except getopt.GetoptError:
        print('cob_build.py -p <PROFILE> -s <SOURCE>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('cob_build.py -p <PROFILE> -s <SOURCE>')
            sys.exit()
        elif opt in ("-p", "--profile"):
            if opt is "":
                print('Error: You must specify a profile')
                sys.exit(2)
            else:
                profile_name = arg
                print('profile_name = ' + profile_name)
        elif opt in ("-s", "--source"):
            if opt is "":
                print('Error: You must specify a COBOL source program')
                sys.exit(2)
            else:
                source_name = arg
                print('source_name = ' + source_name)
    if profile_name is "" or source_name is "":
        print('You must enter both profile and source')
        sys.exit(2)
    else:
        print('source_name: ' + source_name)
        print('profile_name: ' + profile_name)

    listing_1 = Listing(source_name, profile_name)
    parser_1 = Parser(listing_1)

