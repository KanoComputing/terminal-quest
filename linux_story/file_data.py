#!/usr/bin/env python

# file_datas.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Stores permissions of files in a file


import os
import subprocess
import sys
import shutil
from filecmp import dircmp

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from helper_functions import debugger

HOME = os.path.expanduser("~")

FILE_SYSTEM_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "file_system"
)

FILE_SYSTEM_DATA_PATH = os.path.join(FILE_SYSTEM_PATH, "file_system_data")
HIDDEN_DIR = os.path.join(HOME, ".linux-story")


# This is quite slow as it often raises an exception
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def remove_username(abs_path):
    return "/".join(abs_path.split("/")[3:])


def find_last_challenge_path(directory, challenge, step):
    '''Given a challenge number, find the latest file system to copy across
    '''

    # Starting possible path - given a challenge and step number, we
    # check that path straight away
    path = os.path.join(directory, str(challenge), str(step))

    # If path does not exist, look in lower levels
    while not os.path.exists(path):

        # If the step > 1, then have a look at smaller steps
        if int(step) > 1:

            # Rename the path variable that keeps us in this while loop
            step = str(int(step) - 1)
            path = os.path.abspath(os.path.join(directory, challenge, step))

        # If the step is 1, go down to the next challenge
        elif int(step) == 1:

            challenge = str(int(challenge) - 1)
            challenge_path = os.path.abspath(
                os.path.join(
                    directory, challenge
                )
            )

            # If the next challenge down exists, then find the latest step
            # inside
            if os.path.exists(challenge_path):
                step = 1
                for dirs in next(os.walk(challenge_path))[1]:
                    for d in dirs:
                        if int(d) > step:
                            step = int(d)

                path = os.path.join(challenge_path, str(step))

                debugger("path = {}".format(path))

            # Otherwise, create a path with this latest challenge and the
            # step = 1
            else:
                path = os.path.join(challenge_path, '1')

            # If the challenge number is less than 1, then we have no file data
            if int(challenge) < 1:
                raise Exception("No challenges have been provided!")

    return path


def copy_data(challenge_number=1, step_number=1, fork=None):
    '''Copy the relevent file system from the python package into the
    .linux_story directory
    '''

    debugger("copy_data entered")
    debugger(
        "challenge_number = {}, step_number = {}".format(
            challenge_number, step_number
        )
    )
    copy_differences(challenge_number, step_number, fork)

    # Needs to be updated for inclusion of step and forks
    # apply_permissions_to_file_system(challenge_number)


def get_fork_path(path, fork):
    if os.path.exists(path):
        immediate_dirs = [name for name in os.listdir(path)
                          if os.path.isdir(os.path.join(path, name))]
        debugger('immediate_dirs = {}'.format(immediate_dirs))
        for d in immediate_dirs:
            if len(d) == 1:

                # fork options
                # get fork, otherwise default is 'a'
                if not fork:
                    fork = 'a'

                return os.path.join(path, fork)

        return path


def copy_differences(challenge, step, fork):
    '''This changes the file tree in .linux-story by looking at the
    differences between it amd the stored file tree for that challenge
    '''

    debugger(
        'copy_differences, challenge = {}, step = {}'.format(
            str(challenge), str(step)
        )
    )
    challenge_path = find_last_challenge_path(
        FILE_SYSTEM_PATH, str(challenge), str(step)
    )
    fork_path = get_fork_path(challenge_path, fork)
    debugger('fork_path = {}'.format(fork_path))

    dcmp = dircmp(HIDDEN_DIR, fork_path)
    # dcmp = dircmp(HIDDEN_DIR, challenge_path)

    def recursive_bit(dcmp):

        # for each file only in .linux_story, remove it
        for name in dcmp.left_only:
            path = os.path.join(dcmp.left, name)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

        # for each file only in stored challenge file tree,
        # copy it across
        for name in dcmp.right_only:
            copy_from = os.path.join(dcmp.right, name)
            if os.path.isfile(copy_from):
                copy_to = dcmp.left
                shutil.copy(copy_from, copy_to)
            elif os.path.isdir(copy_from):
                copy_to = os.path.join(dcmp.left, name)
                shutil.copytree(copy_from, copy_to)

        # Repeat for the subdirectories
        for sub_dcmp in dcmp.subdirs.values():
            recursive_bit(sub_dcmp)

    recursive_bit(dcmp)


def delete_file_tree():
    filetree = os.path.join(os.path.expanduser("~"), ".linux-story")
    if os.path.exists(filetree):
        shutil.rmtree(filetree)


def generate_rel_path(abs_path):
    dirs = abs_path.split("/")[8:]
    rel_path = "/".join(dirs).strip()
    return rel_path


def list_users():
    '''In bash, list users with:
    cat /etc/passwd | grep "/home" | grep "bin/bash" | cut -d: -f1
    '''

    cat_process = subprocess.Popen(
        ['cat', '/etc/passwd'],
        stdout=subprocess.PIPE
    )

    grep_process = subprocess.Popen(['grep', '/home'],
                                    stdin=cat_process.stdout,
                                    stdout=subprocess.PIPE)
    grep_process_2 = subprocess.Popen(["grep", '/bin/bash'],
                                      stdin=grep_process.stdout,
                                      stdout=subprocess.PIPE)
    cut_process_output = subprocess.check_output(['cut', '-d:', '-f1'],
                                                 stdin=grep_process_2.stdout)
    return cut_process_output.split('\n')


def get_current_user():
    return os.path.expanduser('~').split("/")[2]
