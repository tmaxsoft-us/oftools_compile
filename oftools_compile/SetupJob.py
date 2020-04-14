from .Job import Job


class SetupJob(Job):

    def __init__(self):
        return

    def run(self, in_file):
        print('run SetupJob')

        # create_workdir
        # move source to workdir
        # change directory to workdir

        out_file = in_file.rsplit('/', 1)[1]

        return 0, out_file
