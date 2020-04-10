import os
import sys
from datetime import datetime
from pathlib import Path


class Listing:
    # The below line will be uncommented for actual testing
    # compile_dir = "$OPENFRAME_HOME"
    # Below is the temporary compile_dir for testing
    def __init__(self, source_name, profile):
        compile_dir = os.environ.get('COMPILE_HOME')
        if compile_dir is None:
            sys.exit(255)
        compile_dir += "/listing"
        
        print("Instantiating Listing Object...")
        self.source_name = source_name.rsplit('/', 1)[1]
        self.check_dir_create(compile_dir)
        self.listing_dir = compile_dir + self.source_name + self.get_current_time()
        self.check_dir_create(self.listing_dir)
        self.log_file = os.path.join(self.listing_dir,
                                     source_name + '_log.txt')
        self.temp_dir = os.path.join(self.listing_dir, "temps")
        self.check_dir_create(self.temp_dir)
        self.profile = profile

    def log_append(self, info):
        fw = open(self.log_file, 'a+')
        fw.write(info + '\n')
        fw.close()

    @staticmethod
    def check_profile(profile):
        if os.path.isfile(profile):
            pass
        else:
            print('The profile passed does not exist')
            sys.exit(2)

    @staticmethod
    def check_dir_create(directory):
        if os.path.isdir(directory):
            print('The Directory: ' + directory + ' already exists')
        else:
            os.mkdir(directory)

    @staticmethod
    def get_current_time():
        now = datetime.now()
        return now.strftime("_%Y%m%d_%H%M%S")
