from .Job import Job
import shutil
import os


class DeployJob(Job):

    def __init__(self, config):
        for opt in config.options('deploy'):
            if opt == "volume":
                self.volumes = config.get('deploy', 'volume')
                self.split_volumes = self.volumes.split(':')
                for volume in self.split_volumes:
                    # TODO Error handle for volume does not exist.
                    if not os.path.isdir(volume):
                        os.makedirs(volume)
            elif opt == "region":
                self.region = config.get('deploy', 'region')
        return

    def run(self, in_file):
        print('run DeployJob')
        base_name = self.get_base_name(in_file)
        for volume in self.split_volumes:
            shutil.copy(base_name + ".so", volume)
        out_file = in_file

        return 0, out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]