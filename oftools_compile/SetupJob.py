import os
import shutil
from datetime import datetime

from .Logger import MyLogger
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
        print(in_file)
        print(os.getcwd())
        # Create the name for the workdir by adding suffix to in_file
        in_file_time = in_file.rsplit('/', 1)[1] + self.nowsuffix
        cur_workdir = os.path.join(self.workdir, in_file_time)
        # create_workdir
        if not os.path.isdir(cur_workdir):
            os.mkdir(cur_workdir)
        # copy source to workdir
        shutil.copy(in_file, cur_workdir)
        # change directory to workdir
        os.chdir(cur_workdir)
        # Create logger object
        self._logger = MyLogger.__call__().get_logger()
        self._logger.info("Run SetupJob")
        self._logger.info("SetupJob Completed")
        del self._logger

        out_file = in_file.rsplit('/', 1)[1]

        return 0, out_file
