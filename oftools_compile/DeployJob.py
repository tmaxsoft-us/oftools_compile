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
                self.split_regions = self.region.split(':')
                for region in self.split_regions:
                    # TODO Error handle for region that does not exist
                    if not os.path.isdir(region):
                        os.makedirs(region)
        return

    def run(self, in_file):
        print('run DeployJob')
        print('in_file: ' + in_file)
        base_name = self.get_base_name(in_file)
        out_file = base_name + '.so'
        for volume in self.split_volumes:
            shutil.copy(in_file, os.path.join(volume, out_file))
        for region in self.split_regions:
            shutil.copy(in_file, os.path.join(region, out_file))
        return 0, out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]