#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Description of the class in one sentence.

Description more in details.
"""
# Generic/Built-in modules
import shutil
import os
import subprocess

# Third-party modules

# Owned modules
from .Job import Job
from .Log import Log


class DeployJob(Job):

    def __init__(self, profile):
        self._profile = profile
        return

    def _process_region(self, out_file):

        if self._profile.has_option('deploy', 'region') is False:
            return

        try:
            regions = self._profile.get('deploy', 'region').split(':')
            for region in regions:
                shell_cmd = 'osctdlupdate'
                shell_cmd += ' ' + region
                shell_cmd += ' ' + self._get_base_name(out_file)
                Log().get().info("deploy region: " + shell_cmd)
                proc = subprocess.Popen([shell_cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                out, err = proc.communicate()

                # handle resultget
                if proc.returncode != 0:
                    Log().get().error(out.decode('utf-8'))
                    Log().get().error(err.decode('utf-8'))
                    exit(proc.returncode)
        except:
            Log().get().error('Failed to deploy to region ' + region)

        return

    def _process_tdl(self, out_file):
        if self._profile.has_option('deploy', 'tdl') is False:
            return

        tdls = self._profile.get('deploy', 'tdl').split(':')
        for tdl in tdls:
            shell_cmd = 'cp ' + out_file + ' ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')
            shell_cmd += '; '
            shell_cmd += 'tdlupdate'
            shell_cmd += ' -m ' + self._get_base_name(out_file)
            shell_cmd += ' -r ' + os.path.join(
                os.path.expandvars(tdl) + '/tdl/mod')
            Log().get().info("deploy tdl: " + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle resultget
            if proc.returncode != 0:
                Log().get().error(out.decode('utf-8'))
                Log().get().error(err.decode('utf-8'))
                exit(proc.returncode)

        return

    def _process_dataset(self, out_file):
        out = ""
        err = ""

        if self._profile.has_option('deploy', 'dataset') is False:
            return

        datasets = self._profile.get('deploy', 'dataset').split(':')
        for dataset in datasets:
            shell_cmd = 'dlupdate ' + os.path.join(os.getcwd(),
                                                   out_file) + ' ' + dataset
            Log().get().info("deploy dataset: " + shell_cmd)
            proc = subprocess.Popen([shell_cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            out, err = proc.communicate()

            # handle resultget
            if proc.returncode != 0:
                Log().get().error(out.decode('utf-8'))
                Log().get().error(err.decode('utf-8'))
                exit(proc.returncode)
        """
        try:
            datasets = self._profile.get('deploy', 'dataset').split(':')
            for dataset in datasets:
                shell_cmd = 'dlupdate ' + os.path.join(os.getcwd(),
                                                       out_file) + ' ' + dataset
                Log().get().info("shell command: " + shell_cmd)
                proc = subprocess.Popen([shell_cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                out, err = proc.communicate()

                Log().get().info('rc = ' + proc.returncode)

                # handle resultget
                if proc.returncode != 0:
                    Log().get().error(out.decode('utf-8'))
                    Log().get().error(err.decode('utf-8'))
                    exit(proc.returncode)
        except:
            Log().get().error('Failed to deploy to dataset ')
            Log().get().error(out.decode('utf-8'))
            Log().get().error(err.decode('utf-8'))
        """
        return

    def _rename(self, in_file):
        out_file = in_file

        try:
            out_file = self._profile.get('deploy', 'file')

            Log().get().debug(in_file)
            Log().get().debug(out_file)
            out_file = out_file.replace("$BASENAME",
                                        self._get_base_name(in_file))

            Log().get().debug('rename: ' + out_file)
            shutil.move(in_file, out_file)

        except:
            Log().get().error('failed to rename')

        return out_file

    def run(self, in_file):
        Log().get().debug("Run DeployJob")
        Log().get().debug("in_file: " + in_file)

        # rename the out file for deployment
        out_file = self._rename(in_file)

        # deploy files
        self._process_dataset(out_file)
        self._process_tdl(out_file)
        self._process_region(out_file)

        Log().get().info(out_file + " deploy success")

        return out_file

    def _get_base_name(self, in_file):
        return in_file.rsplit('.', 1)[0]