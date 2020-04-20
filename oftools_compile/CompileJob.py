from .Job import Job
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
        print('run CompileJob')
        print('in_file: ' + in_file)
        base_name = self.get_base_name(in_file)
        out_file = base_name + '.ofcob'
        self.full_command = self.command + " "    \
                          + self.options + " -o " \
                          + out_file + " "        \
                          + in_file
        print(os.getcwd())
        # TODO Replace with log command
        print(self.full_command)
        # TODO Use subprocess to call ofcob and create .ofcob out_file
        # subprocess.call([self.full_command])
        # subprocess.call(['touch', 'add01.ofcob'])
        subprocess.run(self.full_command, shell=True)
        print(out_file)
        return 0, out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]