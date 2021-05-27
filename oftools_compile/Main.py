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
        _create_jobs(profile): Job creation depending on the section of the profile.
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
        parser = argparse.ArgumentParser(
            add_help=False,
            description='OpenFrame Tools Compile')
        parser._action_groups.pop()
        required = parser.add_argument_group('Required arguments')
        optional = parser.add_argument_group('Optional arguments')

        # Required arguments
        required.add_argument(
            '-p',
            '--profile',
            action='append',
            dest='profile_list',
            help='name of the profile, contains the description of the compilation target',
            metavar='PROFILE',
            required=True,
            type=str)

        required.add_argument(
            '-s',
            '--source',
            action='append',
            dest='source_list',
            help='name of the source, either a file or a directory',
            metavar='SOURCE',
            required=True,
            type=str)

        # Optional arguments
        optional.add_argument(
            '-g',
            '--grouping',
            action='store_true',
            dest='grouping',
            help=
            'put all the compilation folders in a single one for mass compilation and aggregate all the logs',
            required=False)

        optional.add_argument(
            '-l',
            '--log-level',
            action='store',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            default='INFO',
            dest='log_level',
            help='set log level, potential values: DEBUG, INFO, WARNING, ERROR, CRITICAL. (default: INFO)',
            metavar='LEVEL',
            required=False,
            type=str)

        optional.add_argument(
            '-t',
            '--tag',
            action='store',
            dest='tag',
            help='add a tag to the name of the report file and the listing directory',
            metavar='TAG',
            required=False,
            type=str)

        optional.add_argument('-h',
                              '--help',
                              action='help',
                              help='show this help message and exit')

        optional.add_argument(
            '-v',
            '--version',
            action='version',
            help='show this version message and exit',
            version='%(prog)s {version}'.format(version=__version__))

        # Deprecated arguments
        optional.add_argument('-r',
                              '--recursive',
                              action='store_false',
                              help=argparse.SUPPRESS)

        optional.add_argument('-e',
                              '--export',
                              action='store_false',
                              help=argparse.SUPPRESS)

        # Do the parsing
        args = parser.parse_args()

        # Analyze number of profiles and sources provided
        if len(args.profile_list) != len(args.source_list):
            Log().logger.critical(
                'The number of profile and source pairs does not match. profile='
                + str(len(args.profile_list)) + ',source=' +
                str(len(args.source_list)))
            exit(-1)

        # Analyze profiles, making sure a file with .prof extension is specified
        for profile in args.profile_list:
            profile_path = os.path.expandvars(profile)

            if os.path.isfile(profile_path):
                extension = profile_path.split('.')[1]
                if extension != 'prof':
                    Log().logger.critical(
                        'Invalid profile. Please specify a file with a .prof extension.'
                    )
                    exit(-1)
            else:
                Log().logger.critical('Cannot access profile: ' + profile)
                exit(-1)

        # Analyze sources
        for source in args.source_list:
            if os.path.exists(os.path.expandvars(source)) is False:
                Log().logger.critical('Cannot access source: ' + source)
                exit(-1)

        # Analyze log level
        if args.log_level:
            if args.log_level not in ('DEBUG', 'INFO', 'WARNING', 'ERROR',
                                      'CRITICAL'):
                Log().logger.warning(
                    'Invalid log level. Using default log level: INFO.')

        return args

    def _create_jobs(self, profile):
        """Job creation depending on the section of the profile.

        Running the method 'sections' on the profile which is a ConfigParser object allow us to create a list of strings, the name of each section of the profile.

        Args:
            profile: A ConfigParser object, the compilation profile specified for the current source.

        Returns:
            A list of Job objects.

        Raises:
        """
        jobs = []
        job_factory = JobFactory(profile)

        for section_name in profile.sections:
            try:
                job = job_factory.create(section_name)
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

        Raises:
            KeyboardInterrupt:
        """
        rc = 0

        # Parse command-line options
        args = self._parse_arg()

        # Handle version option
        if args.version == True:
            return 0

        # Set log level
        Log().set_level(args.log_level)
        Log().open_stream()

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
            Log().logger.debug('Profile path: ' + profile_path)

            # Create jobs
            jobs = self._create_jobs(profile)

            # Source processing
            source = Source(args.source_list[i])
            Log().logger.debug('Source path: ' +
                               os.path.expandvars(args.source_list[i]))

            for source_file in source.files:
                # Initialization of variables before running the jobs
                rc = 0
                file_name_in = ''
                file_name_out = source_file
                start_time = time.time()

                for job in jobs:
                    last_job = job
                    try:
                        # For the SetupJob, file_name_in is an absolute path, but for all other jobs this is just the name of the file
                        file_name_in = file_name_out
                        file_name_out = job.run(file_name_in)
                        rc = 0
                    except KeyboardInterrupt:
                        Log().logger.error(
                            'Keyboard Interrupt: Execution ended by user.')
                        rc = 255
                        #? Why break here and also the one below? Why not just exit?
                        break
                        # exit(1)
                    except:
                        #! Talk about that change
                        Log().logger.exception('')
                        # trace_list = traceback.format_exc().splitlines()
                        # for trace in trace_list:
                        #     Log().logger.error(trace)
                        rc = -3
                        break

                # Stop above for loop when Ctrl + C
                if rc == -255:
                    break

                # Elapsed time calculation
                elapsed_time = time.time() - start_time

                report.add_entry(source_file, last_job, rc, elapsed_time)

                #? Why storing all the working directories in a list? For the grouping feature.
                Context().add_workdir()
                Context().clear()
                Log().close_file()

                if rc != 0:
                    break

        report.generate()

        # Handle grouping option
        if args.grouping == True:
            grouping = Grouping()
            grouping.run()

        # Need to clear context and log to run pytest
        Context().clear()
        Log().close_stream()

        return rc
