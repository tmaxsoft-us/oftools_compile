import os
import shutil
from datetime import datetime

from .Job import Job


class SetupJob(Job):
    base_dir = os.environ.get("OPENFRAME_HOME")
    listing_dir = os.path.join(base_dir, "cob_listings")

    def __init__(self):
        self.now = datetime.now()
        self.nowsuffix = self.now.strftime("_%Y%m%d_%H%M%S")
        return

    def run(self, in_file):
        print('run SetupJob')

        # create_workdir
        time_workdir = in_file.rsplit('/', 1)[1] + self.nowsuffix
        workdir = os.path.join(self.listing_dir, time_workdir)
        os.mkdir(workdir)
        tempdir = os.path.join(workdir, "temps")
        os.mkdir(tempdir)
        logdir = os.path.join(workdir, "logs")
        os.mkdir(logdir)
        # copy source to workdir
        shutil.copy(in_file, tempdir)
        # change directory to workdir
        os.chdir(str(workdir))

        out_file = in_file.rsplit('/', 1)[1]

        return 0, out_file
