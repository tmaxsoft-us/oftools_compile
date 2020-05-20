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
import time
from configparser import ConfigParser

# Third-party modules

# Owned modules
from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob
from .Log import Log
from .Utils import Utils


class Main:

    def __init__(self):
        return

    def _create_jobs(self, profile):
        jobs = []
        job_factory = JobFactory(profile)
        for section in profile.sections():
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
                                help='name of the source which must be a file.',
                                required=True)

        arg_parser.add_argument(
            '-p',
            '--profile',
            help=
            'Path to the profile which contains description of the compilation target.',
            required=True)

        arg_parser.add_argument(
            '-i',
            '--import',
            help=
            'import csv formatted manifest which contains source and profile.',
            required=False)

        arg_parser.add_argument(
            '-l',
            '--log',
            help='set log level (DEBUG|INFO|WARNING|ERROR|CRITICAL).',
            required=False)

        # do the parsing
        args = arg_parser.parse_args()

        # analyze parsing result
        if os.path.isfile(os.path.expandvars(args.profile)) is False:
            print('cannot access profile: ' + args.profile)
            exit(-1)

        if os.path.isfile(os.path.expandvars(args.source)) is False:
            print('cannot access source: ' + args.source)
            exit(-1)

        return args

    def run(self):
        rc = 0

        # parse inline command
        args = self._parse_arg()

        # set log level
        Log().set_level(args.log)

        # start time
        start_time = time.time()

        # read profile
        profile = ConfigParser()
        profile.optionxform = str
        profile.read(os.path.expandvars(args.profile))

        # clear context of Utils
        Utils().clear()

        # run jobs
        in_file = ""
        out_file = args.source
        jobs = self._create_jobs(profile)
        for job in jobs:
            try:
                in_file = out_file
                out_file = job.run(in_file)
            except:
                traceback.print_exc()
                rc = -3
                break

        end_time = time.time()

        Log().get().info('elapsed time: ' + str(end_time - start_time))

        return rc
