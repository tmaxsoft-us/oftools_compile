import os
import shutil
from datetime import datetime

from .Job import Job


class SetupJob(Job):

    def __init__(self, config):
        user_home = os.getenv("HOME")
        for opt in config.options('setup'):
            if opt == "workdir":
                self.workdir = config.get('setup', 'workdir')
                self.workdir = self.workdir.replace("~", user_home)
                if not os.path.isdir(self.workdir):
                    os.mkdir(self.workdir)
                print(self.workdir)
        self.now = datetime.now()
        self.nowsuffix = self.now.strftime("_%Y%m%d_%H%M%S")
        return

    def run(self, in_file):
        print('run SetupJob')

        # create_workdir
        in_file_time = in_file.rsplit('/', 1)[1] + self.nowsuffix
        cur_workdir = os.path.join(self.workdir, in_file_time)
        os.mkdir(cur_workdir)
        tempdir = os.path.join(cur_workdir, "temps")
        os.mkdir(tempdir)
        logdir = os.path.join(cur_workdir, "logs")
        os.mkdir(logdir)
        # copy source to workdir
        shutil.copy(in_file, tempdir)
        # change directory to workdir
        os.chdir(cur_workdir)

        out_file = in_file.rsplit('/', 1)[1]

        return 0, out_file
