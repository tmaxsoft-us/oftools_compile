from .Job import Job
from .Logger import MyLogger
import subprocess
import shutil
import os


class CompileJob(Job):

    def __init__(self, section, config):
        if section == 'ofcob':
            self.command = 'ofcob'
            for opt in config.options('ofcob'):
                if opt == "option":
                    self.options = config.get('ofcob', 'option')
        return

    def run(self, in_file):
        self._logger = MyLogger.__call__().get_logger()
        self._logger.info("Run CompileJob")
        self._logger.info("in_file: " + in_file)
        base_name = self.get_base_name(in_file)
        out_file = base_name + '.ofcob'
        self.full_command = self.command + " "    \
                          + self.options + " -o " \
                          + out_file + " "        \
                          + in_file
        # print(self.full_command)
        self._logger.info("Full Command: " + self.full_command)
        subprocess.run(self.full_command, shell=True)
        self._logger.info("out_file: " + out_file)
        del self._logger
        return 0, out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]