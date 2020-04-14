from .Job import Job


class CompileJob(Job):

    def __init__(self):
        return

    def run(self, in_file):
        out_file = in_file
        print('run CompileJob')

        return 0, out_file