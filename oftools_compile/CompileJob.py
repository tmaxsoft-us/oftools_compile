from .Job import Job
import subprocess


class CompileJob(Job):

    def __init__(self, section, config):
        if section == 'ofcob':
            self.command = 'ofcob'
            for opt in config.options('ofcob'):
                if opt == "option":
                    self.options = config.get('ofcob', 'option')
                    print(self.options)
        return

    def run(self, in_file):
        out_file = in_file
        print('run CompileJob')
        # subprocess.call([self.command, in_file, self.options])
        print(self.command + " " + in_file + " " + self.options)
        return 0, out_file