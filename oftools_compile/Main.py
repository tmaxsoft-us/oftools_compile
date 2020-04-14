import os
import argparse
import traceback

from configparser import ConfigParser

from .Profile import Profile

from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob


class Main:

    def __init__(self):
        return

    def run(self):
        rc = 0

        # read stdin & profile
        try:
            # get profile_path and source_path
            profile_path, source_path = self._parse_arg()

            # get config
            config = ConfigParser()
            config.read(profile_path)
        except:
            traceback.print_exc()
            return -1

        # create profiles
        profiles = []
        for section in config.sections():
            try:
                options = config.options(section)
                profile = Profile(section, options)
                profiles.append(profile)
            except:
                traceback.print_exc()
                return -1

        # create jobs
        jobs = []
        job_factory = JobFactory()
        for profile in profiles:
            try:
                job = job_factory.create(profile)
                jobs.append(job)
            except:
                traceback.print_exc()
                return -2

        # analyze created jobs
        if job_factory.isFine() is not True:
            print('Missing jobs found. abort!')
            return -2

        # run jobs
        in_file = ""
        out_file = source_path
        for job in jobs:
            try:
                in_file = out_file
                rc, out_file = job.run(in_file)

                if rc is not 0:
                    break
            except:
                traceback.print_exc()
                return -3

        return rc

    def _parse_arg(self):

        # add parse arguments
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-s',
                                '--source',
                                help='source code path',
                                required=True)
        arg_parser.add_argument('-p',
                                '--profile',
                                help='profile path',
                                required=True)

        # do the parsing
        args = arg_parser.parse_args()

        # analyze parsing result
        if os.path.isfile(args.profile) is False:
            print('profile does not exist')
            exit(-1)

        if os.path.isfile(args.source) is False:
            print('source does not exist')
            exit(-1)

        return args.profile, args.source