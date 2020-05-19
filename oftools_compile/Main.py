#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import os
import argparse
import traceback
import sys
from configparser import ConfigParser

# Third-party modules

# Owned modules
from .Config.Profile import Profile
from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob


class Main:

    def __init__(self):
        return

    def _create_jobs(self, config):
        jobs = []
        job_factory = JobFactory(config)
        for section in config.sections():
            try:
                job = job_factory.create(section)
                jobs.append(job)
            except:
                traceback.print_exc()
                print('Unexpected error detected during the job creation')
                exit(-1)

        # analyze created jobs
        if job_factory.is_fine() is not True:
            print('Missing jobs found. abort!')
            exit(-1)

        return jobs

    def _parse_arg(self):
        # add parse arguments
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('-s',
                                '--source',
                                help='Source path. Source must be a file.',
                                required=True)

        arg_parser.add_argument(
            '-p',
            '--profile',
            help=
            'Path to the profile which contains description of the compilation target.',
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

        return args

    def run(self):
        rc = 0

        # parse inline command
        args = self._parse_arg()

        # read config
        config = ConfigParser()
        config.read(args.profile)

        # create jobs
        jobs = self._create_jobs(config)

        # run jobs
        in_file = ""
        out_file = args.source
        for job in jobs:
            try:
                in_file = out_file
                out_file = job.run(in_file)
            except:
                traceback.print_exc()
                return -3

        return rc
