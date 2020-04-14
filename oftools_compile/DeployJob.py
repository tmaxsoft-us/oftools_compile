from .Job import Job


class DeployJob(Job):

    def __init__(self):
        return

    def run(self, in_file):
        print('run DeployJob')
        out_file = in_file

        return 0, out_file
