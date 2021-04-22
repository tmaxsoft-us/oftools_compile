#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main module of OpenFrame Tools Compile.
"""
# Generic/Built-in modules
import os
import argparse
import traceback
import time

# Third-party modules

# Owned modules
from . import __version__
from .Context import Context
from .Grouping import Grouping
from .JobFactory import JobFactory
from .Log import Log
from .Profile import Profile
from .Report import Report
from .Source import Source


def main():
    return Main().run()


class Main:
    """Main class containing the methods for parsing the command arguments and running OpenFrame Tools Compile.

    Methods:
        _parse_arg(): Parsing command-line options.
        _create_jobs(): Job creation depending on the section of the profile.
        _run_internal(profile, source, report_generator): More details about which jobs are 
            actually running during compilation.
        run(): Perform all the steps to run compilation for all sources using the appropriate 
            profile.
    """

    def _parse_arg(self):
        """Parsing command-line options.

        The program defines what arguments it requires, and argparse will figure out how to parse 
        those out of sys.argv. The argparse module also automatically generates help and usage 
        messages and issues errors when users give the program invalid arguments.

        Returns:
            args, an ArgumentParser object.
        """
        arg_parser = argparse.ArgumentParser()

        # Mandatory arguments
        arg_parser.add_argument(
            '-p',
            '--profile',
            action='append',
            dest='profile_list',
            help='Profile which contains description of the compilation target',
            metavar='PROFILE',
            required=True)

        arg_parser.add_argument('-s',
                                '--source',
                                action='append',
                                dest='source_list',
                                help='Name of the source which must be a file',
                                metavar='SOURCE',
                                required=True)

        # Optional arguments
        arg_parser.add_argument(
            '-g',
            '--grouping',
            action='store_true',
            dest='grouping',
            help=
            'Put all the compilation folders in a single one for mass compilation and aggregate all the logs',
            required=False)

        arg_parser.add_argument(
            '-l',
            '--log-level',
            action='store',
            default='INFO',
            dest='log_level',
            help=
            'Set log level (DEBUG|INFO|WARNING|ERROR|CRITICAL). Default is INFO',
            metavar='LEVEL',
            required=False)

        arg_parser.add_argument(
            '-t',
            '--tag',
            action='store',
            dest='tag',
            help='Add tag to the name of report file and the listing directory',
            metavar='TAG',
            required=False)

        arg_parser.add_argument('-v',
                                '--version',
                                action='store_true',
                                help='Print version information',
                                required=False)

        # Deprecated arguments
        arg_parser.add_argument('-r',
                                '--recursive',
                                action='store_false',
                                help=argparse.SUPPRESS)

        arg_parser.add_argument('-e',
                                '--export',
                                action='store_false',
                                help=argparse.SUPPRESS)

        # Do the parsing
        args = arg_parser.parse_args()

        # Handle version option
        if args.version is True:
            version = 'oftools-compile ' + __version__
            print(version)
            return args

        # Analyze parsing result and handle errors
        if args.profile_list is None:
            Log().get().critical('-p or --profile option is not specified')
            exit(-1)

        if args.source_list is None:
            Log().get().critical('-s or --source option is not specified')
            exit(-1)

        if len(args.profile_list) != len(args.source_list):
            Log().get().critical(
                'The number of profile and source pairs does not match. profile='
                + str(len(args.profile_list)) + ',source=' +
                str(len(args.source_list)))
            exit(-1)

        for profile in args.profile_list:
            if os.path.isfile(os.path.expandvars(profile)) is False:
                Log().get().critical('Cannot access profile: ' + profile)
                exit(-1)

        for source in args.source_list:
            if os.path.exists(os.path.expandvars(source)) is False:
                Log().get().critical('Cannot access source: ' + source)
                exit(-1)

        return args

    def _create_jobs(self, profile):
        """Job creation depending on the section of the profile.

        Running the method 'sections' on the profile which is a ConfigParser object allow us to create a list of strings, the name of each section of the profile.

        Args:
            profile: A ConfigParser object, the compilation profile specified for the current source.

        Returns:
            A list of Job objects.
        """
        jobs = []
        job_factory = JobFactory(profile)

        for section in profile.sections:
            try:
                job = job_factory.create(section)
                jobs.append(job)
            except:
                traceback.print_exc()
                print('Unexpected error detected during the job creation.')
                exit(-1)

        return jobs

    def run(self):
        """Perform all the steps to run compilation for all sources using the appropriate 
        profile.

        Returns:
            An integer, the return code of the program.
        """
        rc = 0

        # Parse command-line options
        args = self._parse_arg()

        # Handle version option
        if args.version is True:
            return 0

        # Set log level
        Log().set_level(args.log_level)

        Context().tag(args.tag)

        report = Report()

        profile_dict = {}

        # Run compilation through sources
        for i in range(len(args.source_list)):
            # Profile processing
            profile_path = os.path.expandvars(args.profile_list[i])
            
            if profile_path not in profile_dict.keys():
                profile = Profile(profile_path)
                profile_dict[profile_path] = profile
            else:
                profile = profile_dict[profile_path]
            Log().get().debug('Profile path: ' + profile_path)

            # Create jobs
            jobs = self._create_jobs(profile)

            # Source processing
            source = Source(args.source_list[i])
            Log().get().debug('Source path: ' +
                              os.path.expandvars(args.source_list[i]))

            for source_file in source.files:
                input_name = ''
                output_name = source_file
                rc = 0
                start_time = time.time()

                for job in jobs:
                    last_job = job
                    try:
                        input_name = output_name
                        output_name = job.run(input_name)
                        rc = 0
                    except KeyboardInterrupt:
                        rc = -255
                        break
                    except:
                        trace_list = traceback.format_exc().splitlines()
                        for trace in trace_list:
                            Log().get().error(trace)
                        rc = -3
                        break

                # Stop above for loop when Ctrl + C
                if rc == -255:
                    break

                # Elapsed time calculation
                elapsed_time = time.time() - start_time

                report.add_entry(source_file, last_job, rc, elapsed_time)

                #TODO Move add_workdir in the report module, add_entry method
                Context().add_workdir()
                Context().clear()
                Log().clear()

                if rc != 0:
                    break

        report.generate()

        # Handle grouping option
        if args.grouping is True:
            grouping = Grouping()
            grouping.run()

        # Need to clear context and log to run pytest
        Context().clear()
        Log().clear()

        return rc
