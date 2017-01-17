#! /usr/bin/env python

"""
re-run failed jobs

    >>> ./find_failed.py $ouput_directory $path_to_batchlist
"""

import os
from sys import argv

def has_failed(directory, expected):
    """
    determine if individual job's output is not expected
    """
    # get full-path to directory
    return len(os.listdir(directory)) < expected


def find_failed_jobs(dirs, expected=2):
    """
    return directories for of the failed jobs.
    jobs are failed if the directories do not have the expected number of files

    Parameters:
    ------------
    directory (string):
        directory which contains
    """
    out = []
    for i in os.listdir(dirs):
	full_path = os.path.join(os.path.abspath(dirs), i)
	if has_failed(full_path, expected):
	    out.append(i)
    return out


def commands_for_failed_jobs(failed, batch_list):
    """
    return cellprofiler commands for failed jobs from the original batchlist

    Parameters:
    ------------
    failed (list-like):
        list of failed jobs from find_failed_jobs()
    batch_list (list-like):
        list of cellprofiler commands from original run
    """
    failed_commands = []
    for failed_job in failed:
        for command in batch_list:
            if failed_job in command:
                failed_commands.append(command)
    return failed_commands


if __name__ == "__main__":
    # directory name for output directory
    failed_jobs = find_failed_jobs(dirs=argv[1])

    # open batch commands
    batch_list = open(argv[2], "r").readlines()
    # strip newlines
    batch_list = [i.strip() for i in batch_list]

    failed_commands = commands_for_failed_jobs(failed_jobs, batch_list)

    # print failed_commands to stdout
    for i in failed_commands:
        print(i)
