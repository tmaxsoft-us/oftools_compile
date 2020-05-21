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
from collections import OrderedDict

# Third-party modules

# Owned modules
from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob
from .Log import Log
from .Context import Context
from .ReportGenerator import ReportGenerator


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

        arg_parser.add_argument(
            '-p',
            '--profile',
            help='profile which contains description of the compilation target.',
            required=True)

        arg_parser.add_argument('-s',
                                '--source',
                                help='name of the source which must be a file.',
                                required=True)

        arg_parser.add_argument('-r',
                                '--recursive',
                                action='store_true',
                                help='activate recursive compilation.',
                                required=False)

        arg_parser.add_argument('-e',
                                '--export',
                                action='store_true',
                                help='export the csv formatted report file.',
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
            Log().get().critical('cannot access profile: ' + args.profile)
            exit(-1)

        if os.path.exists(os.path.expandvars(args.source)) is False:
            Log().get().critical('cannot access source: ' + args.source)
            exit(-1)

        if args.recursive:
            if os.path.isfile(os.path.expandvars(args.source)) is True:
                Log().get().critical(
                    'only directory is allowed when -r or --recursive is used')
                exit(-1)
        else:
            if os.path.isfile(os.path.expandvars(args.source)) is False:
                Log().get().critical(
                    'source is a directory. please use -r or --recursive if the source is a directory'
                )
                exit(-1)

        return args

    def run(self):
        # initialize
        rc = 0
        total_time = 0
        source_list = []

        # parse inline command
        args = self._parse_arg()

        # set log level
        Log().set_level(args.log)

        # read profile
        profile = ConfigParser(dict_type=OrderedDict)
        profile.optionxform = str
        profile.read(os.path.expandvars(args.profile))

        Log().get().debug('sections: ' + str(profile.sections()))

        # build source list
        Log().get().debug('arg recursive: ' + str(args.recursive))
        if args.recursive:
            directory = os.path.expandvars(args.source)

            for dirpath, _, filenames in os.walk(directory):
                for f in filenames:
                    source_list.append(os.path.abspath(os.path.join(dirpath,
                                                                    f)))
        else:
            source_list = [args.source]

        Log().get().debug(source_list)

        # run jobs through sources
        report_generator = ReportGenerator()

        last_job = None
        for source in source_list:
            start_time = time.time()
            Context().clear()
            Log().clear()

            in_name = ""
            out_name = source
            jobs = self._create_jobs(profile)

            for job in jobs:
                last_job = job
                try:
                    in_name = out_name
                    out_name = job.run(in_name)
                    rc = 0
                except KeyboardInterrupt:
                    rc = -255
                    break
                except:
                    traceback.print_exc()
                    rc = -3
                    break

            # stop looping when ctrl+c
            if rc == -255:
                break

            unit_time = time.time() - start_time
            Log().get().info('elapsed time: ' + str(round(unit_time, 4)))
            total_time += unit_time

            success = 'Y'
            if rc < 0:
                success = 'N'

            Log().get().debug('rc: ' + str(rc))
            Log().get().debug('success: ' + success)

            last_section = ""
            if Context().is_mandatory_complete() is not True:
                last_section = Context().get_mandatory_section()
            else:
                last_section = last_job.get_section()
                last_index = last_section.find('?')
                if last_index > 0:
                    last_section = last_section[:last_index]
                    Log().get().debug('?:' + last_section)

            report_generator.add(source,
                                 Context().get_cur_workdir(), last_section,
                                 success, unit_time)

        report_generator.generate(args.export)

        return rc
