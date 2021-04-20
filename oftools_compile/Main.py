#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main module of OpenFrame Tools Compile.
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
from . import __version__
from .JobFactory import JobFactory
from .CompileJob import CompileJob
from .SetupJob import SetupJob
from .DeployJob import DeployJob
from .Log import Log
from .Context import Context
from .ReportGenerator import ReportGenerator
from .Grouping import Grouping


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
        for section in profile.sections():
            try:
                job = job_factory.create(section)
                jobs.append(job)
            except:
                traceback.print_exc()
                print('Unexpected error detected during the job creation')
                exit(-1)

        # Analyze created jobs
        if job_factory.is_fine() is False:
            print('Missing jobs found. abort!')
            exit(-1)

        return jobs

    def _run_internal(self, profile_name, source, report_generator):
        """More details about which jobs are actually running during compilation.

        From the source argument, the method checks whether this is a single file or a directory 
        and then create the source list. This method run a job (whether SetupJob, CompileJob or 
        DeployJob) for each section of the profile and for each source. 

        Args:
            profile_name: A string, the compilation profile specified for the current source.
            source: A string, the source for the current compilation, could be a file or a 
                directory.
            report_generator: A ReportGenerator, used to retrieve data about compilation status, 
                success or failed, errors, etc.

        Returns:
            An integer, the return code of the compilation process.
        """
        rc = 0

        # Read profile and create ConfigParser object
        profile = ConfigParser(dict_type=OrderedDict)
        profile.optionxform = str
        profile.read(os.path.expandvars(profile_name))
        Log().get().debug('profile path = ' + os.path.expandvars(profile_name))

        # Check whether source is a file or a folder and then create the source list
        if os.path.isdir(source):
            directory = os.path.expandvars(source)
            source_list = []
            for root, _, files in os.walk(directory):
                if root.startswith('.'):
                    continue
                for name in files:
                    if name.startswith('.'):
                        continue
                    source_list.append(os.path.abspath(os.path.join(root,
                                                                    name)))
        else:
            source_list = [source]

        # Sort the list alphabetically
        source_list.sort()

        # Execute compilation process for each source of the list
        last_job = None
        for source in source_list:
            start_time = time.time()
            Context().clear()
            Log().clear()

            input_file_name = ''
            out_name = source
            jobs = self._create_jobs(profile)

            # For each source there are multiple sections that need to be processed
            # Each section of the compilation profile correspond to a job
            for job in jobs:
                last_job = job
                try:
                    input_file_name = out_name
                    out_name = job.run(input_file_name)
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

            # Is the compilation a success or a failure?
            if rc >= 0:
                compilation_status = 'Y'
            else:
                compilation_status = 'N'

            # Check that last job executed for the current source corresponds to a deploy section
            last_section = last_job._remove_filter_name(last_job.get_section())
            if last_section.startswith('deploy'):
                if Context().is_mandatory_section_complete() is False:
                    last_section = Context().mandatory_section()

            report_generator.add(source,
                                 Context().current_workdir(), last_section,
                                 compilation_status, elapsed_time)

            Context().add_workdir()

        return rc

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
        report_generator = ReportGenerator()

        # Run compilation through sources
        for i in range(len(args.source_list)):
            Log().clear()
            Context().clear()
            rc = self._run_internal(args.profile_list[i], args.source_list[i],
                                    report_generator)
            if rc != 0:
                break

        report_generator.generate()

        # Handle grouping option
        if args.grouping is True:
            grouping = Grouping()
            grouping.run()

        # Need to clear context to run pytest
        Log().clear()
        Context().clear()

        return rc
