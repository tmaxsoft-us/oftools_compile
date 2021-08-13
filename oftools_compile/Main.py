#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main module of OpenFrame Tools Compile.
"""
# Generic/Built-in modules
import argparse
import os
import sys
import traceback
import time
# import logging

# Third-party modules

# Owned modules
from . import __version__
from .Clear import Clear
from .Context import Context
from .Grouping import Grouping
from .JobFactory import JobFactory
from .Log import Log
from .Profile import Profile
from .Report import Report
from .Source import Source


def main():
    return Main().run()


class Main(object):
    """Main class containing the methods for parsing the command arguments and running OpenFrame Tools 
    Compile.

    Methods:
        _parse_args(): Parses command-line options.
        _create_jobs(profile): Creates job depending on the section of the profile.
        run(): Performs all the steps to run compilation for all sources using the appropriate profile.
    """

    def _parse_args(self):
        """Parses command-line options.

        The program defines what arguments it requires, and argparse will figure out how to parse those 
        out of sys.argv. The argparse module also automatically generates help, usage messages and 
        issues errors when users give the program invalid arguments.

        Returns:
            args, an ArgumentParser object.

        Raises:
            TypeError: An error occurs if the file extension of the profile is not .prof.
            SystemError: An error occurs if the numbers of profile and source are not 
                matching.           
        """
        parser = argparse.ArgumentParser(add_help=False,
                                         description='OpenFrame Tools Compile')
        parser._action_groups.pop()
        required = parser.add_argument_group('Required arguments')
        optional = parser.add_argument_group('Optional arguments')
        others = parser.add_argument_group('Help & version')

        # Required arguments
        required.add_argument(
            '-p',
            '--profile',
            action='append',
            dest='profile_list',
            help=
            'name of the profile, contains the description of the compilation target',
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
            '-c',
            '--clear',
            action='store_true',
            dest='clear',
            help='clear all the files generated during compilation',
            required=False)

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
            help=
            'set log level, potential values: DEBUG, INFO, WARNING, ERROR, CRITICAL. (default: INFO)',
            metavar='LEVEL',
            required=False,
            type=str)

        optional.add_argument(
            '--skip',
            action='store_true',
            dest='skip',
            help='set skip flag, used to skip source files if not found',
            required=False)

        optional.add_argument(
            '-t',
            '--tag',
            action='store',
            dest='tag',
            help=
            'add a tag to the name of the report file and the listing directory',
            metavar='TAG',
            required=False,
            type=str)

        # Other arguments
        others.add_argument('-h',
                            '--help',
                            action='help',
                            help='show this help message and exit')

        others.add_argument(
            '-v',
            '--version',
            action='version',
            help='show this version message and exit',
            version='%(prog)s {version}'.format(version=__version__))

        # Deprecated arguments
        optional.add_argument('-r',
                              '--recursive',
                              action='store',
                              help=argparse.SUPPRESS)

        optional.add_argument('-e',
                              '--export',
                              action='store',
                              help=argparse.SUPPRESS)

        # Do the parsing
        if len(sys.argv) == 1:
            parser.print_help(sys.stdout)
            sys.exit(0)
        try:
            args = parser.parse_args()
        except argparse.ArgumentError as e:
            Log().logger.critical('ArgumentError: ' + str(e))
            sys.exit(-1)

        # Analyze profiles, making sure a file with .prof extension is specified for each profile
        try:
            for profile in args.profile_list:
                profile_path = os.path.expandvars(profile)
                extension = profile_path.rsplit('.', 1)[1]
                if extension != 'prof':
                    raise TypeError()
        except IndexError:
            Log().logger.critical(
                'IndexError: Given profile does not have a .prof extension: ' +
                profile)
            sys.exit(-1)
        except TypeError:
            Log().logger.critical(
                'TypeError: Expected .prof extension, found ' + extension +
                ': ' + profile)
            sys.exit(-1)

        # Analyze number of profiles and sources provided
        try:
            if len(args.profile_list) != len(args.source_list):
                raise SystemError()
        except SystemError:
            Log().logger.critical(
                'NumberError: Number of profile and source are not matching: profile='
                + str(len(args.profile_list)) + ', source=' +
                str(len(args.source_list)))
            sys.exit(-1)

        return args

    def _create_jobs(self, profile):
        """Creates job depending on the section of the profile.

        Running the method 'sections' on the profile which is a ConfigParser object allow us to create 
        a list of strings, the name of each section of the profile. And then a call to the method 
        create of the JobFactory module generate the corresponding job.

        Args:
            profile: A ConfigParser object, the compilation profile specified for the current source.

        Returns:
            A list of Job objects.

        Raises:
            #TODO Complete docstrings, maybe change the behavior to print traceback only with DEBUG as log level
        """
        jobs = []
        job_factory = JobFactory(profile)

        for section_name in profile.sections:
            try:
                # Log().logger.debug('Creating job for the section: ' +
                #                    section_name)
                job = job_factory.create(section_name)
                jobs.append(job)
            except:
                traceback.print_exc()
                Log().logger.error(
                    'Unexpected error detected during the job creation')
                sys.exit(-1)

        return jobs

    def run(self):
        """Performs all the steps to run compilation for all sources using the appropriate profile.

        Returns:
            An integer, the return code of the program.
        """
        rc = 0
        # For testing purposes. allow to remove logs when executing coverage
        # logging.disable(logging.CRITICAL)
        Log().open_stream()

        # Parse command-line options
        args = self._parse_args()

        # Set log level and log oftools_compile command as DEBUG
        Log().set_level(args.log_level)
        Log().logger.debug(' '.join((arg for arg in sys.argv)))

        # Initialize variables for program execution
        Context().skip = args.skip
        Context().tag = args.tag
        profile_dict = {}
        report = Report()

        for i in range(len(args.source_list)):

            # Profile processing
            profile_path = os.path.expandvars(args.profile_list[i])
            Log().logger.debug('Profile path: ' + profile_path)
            if profile_path not in profile_dict.keys():
                profile = Profile(profile_path)
                profile_dict[profile_path] = profile
            else:
                Log().logger.debug('Profile already used: ' + profile_path +
                                   '. Reusing Python Profile object')
                profile = profile_dict[profile_path]

            # Source processing
            Log().logger.debug('Source path: ' +
                               os.path.expandvars(args.source_list[i]))
            source = Source(args.source_list[i])

            # Create jobs
            jobs = self._create_jobs(profile)

            for file_path in source.file_paths:
                # Initialization of variables before running the jobs
                file_name_in = ''
                file_name_out = file_path
                start_time = time.time()

                for job in jobs:
                    # For the SetupJob, file_name_in is an absolute path, but for all other jobs this
                    # is just the name of the file
                    file_name_in = file_name_out
                    rc = job.run(file_name_in)
                    if rc != 0:
                        Log().logger.error(
                            'An error occurred. Aborting source file processing'
                        )
                        break
                    file_name_out = job.file_name_out

                # Report related tasks
                elapsed_time = time.time() - start_time
                report.add_entry(file_path, rc, elapsed_time)
                # Need to clear return code, context and close log file at the end of each file processing
                rc = 0
                Context().clear()
                Log().close_file()

        if len(source.file_paths) != 0:
            report.summary(args.clear)

            # Handle clear option
            if args.clear is True:
                clear = Clear()
                clear.run()
            elif args.grouping is True:
                grouping = Grouping()
                grouping.run()

        # Need to clear context completely and close log at the end of the execution
        Context().clear_all()
        Log().close_stream()

        return rc