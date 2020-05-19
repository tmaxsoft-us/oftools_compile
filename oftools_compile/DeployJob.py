#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import shutil
import os

# Third-party modules

# Owned modules
from .Job import Job
from .Log import Log


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

    def _deploy_region(self):
        return

    def _deploy_volume(self):
        return

    def run(self, in_file):
        Log().info("Run DeployJob")
        Log().info("in_file: " + in_file)

        base_name = self.get_base_name(in_file)
        out_file = base_name + '.so'

        for volume in self.split_volumes:
            shutil.copy(in_file, os.path.join(volume, out_file))
            Log().info('copy files: src=' + in_file + ' dest=' +
                       os.path.join(volume, out_file))

        for region in self.split_regions:
            shutil.copy(in_file, os.path.join(region, out_file))
            Log().info('copy files: src=' + in_file + ' dest=' +
                       os.path.join(volume, out_file))

        Log().info("out_file: " + out_file)

        return out_file

    @staticmethod
    def get_base_name(in_file):
        return in_file.rsplit('.', 1)[0]