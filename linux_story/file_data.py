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


# TODO: this needs to be changed so if the data is already in the tree
# it is not copied across
# We want to preserve changes made by the user that don't conflict with the
# levels
def copy_data(challenge_number=1, step_number=1):
    '''Copy the relevent file system from the python package into the
    .linux_story directory
    '''

    debugger("copy_data entered")
    debugger(
        "challenge_number = {}, step_number = {}".format(
            challenge_number, step_number
        )
    )
    copy_file_tree(challenge_number, step_number)

    """pfile = get_permission_file(challenge_number)
    debugger("Entering pfile = {}".format(pfile))

    with open(pfile, 'r') as permissionsfile:
        for line in permissionsfile:
            elements = line.split(" ")
            permission_list = elements[0]
            path = elements[-1]
            rel_path = generate_rel_path(path)
            file_owner = elements[1]
            group_owner = elements[2]

            real_loc = os.path.join(os.path.expanduser("~"), (".linux-story"))

            change_permissions(permission_list, rel_path, real_loc)
            change_ownership(file_owner, group_owner, rel_path, real_loc)"""


def copy_selected_data(challenge=1, step=1):
    '''Only copy across the files that are missing
    Takes the challenge and step numbers and finds the corresponding filetree

    The directory we're looking for takes the form:
    "file_system/<step_number>_<challenge_number>"
    e.g. "file_system/1_3"
    '''

    dir_name = str(challenge) + '_' + str(step)
    challenge_dir = os.path.join(FILE_SYSTEM_PATH, dir_name)

    for src_path, src_dirs, src_files in os.walk(challenge_dir):
        rel_path = src_path.replace(challenge_dir + "/", "")
        for d in src_dirs:
            dest_dir = os.path.join(HIDDEN_DIR, rel_path, d)
            exists = os.path.exists(dest_dir)
            if not exists:
                src_dir = os.path.join(src_path, d)

                debugger(
                    "\ncopying from \n{} to \n{}".format(
                        src_dir, dest_dir
                    )
                )

                # We include symlinks for later challenges which
                # could involve them
                shutil.copytree(src_dir, dest_dir, symlinks=True)
        for f in src_files:
            dest_file = os.path.join(HIDDEN_DIR, rel_path, f)
            exists = os.path.exists(dest_file)
            if not exists:
                src_file = os.path.join(src_path, f)

                debugger(
                    "\ncopying from \n{} to \n{}".format(
                        src_file, dest_file
                    )
                )

                shutil.copyfile(src_file, dest_file)


def copy_file_tree(challenge=1, step=1):
    '''Copy files over from root to the home
    Takes the integers challenge and the step
    '''

    debugger("copy_file_tree entered")
    debugger("challenge = {}, step = {}".format(challenge, step))

    path = find_last_challenge_path(FILE_SYSTEM_PATH, challenge, step)
    delete_file_tree()

    try:
        shutil.copytree(path, HIDDEN_DIR)
    except:
        debugger("copy_file_tree failed")
        debugger("Unexpected error:", sys.exc_info()[0])
        pass


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


"""def get_permission_file(challenge=1, step=1):
    debugger(
        "get_permssions_file, challenge_number = {}".format(
            challenge
        )
    )

    if not os.path.exists(FILE_SYSTEM_DATA_PATH):
        os.makedirs(FILE_SYSTEM_DATA_PATH)

    path = find_last_challenge_path(FILE_SYSTEM_DATA_PATH, challenge, step)
    return path"""


# TODO: change this so that it goes through the challenge dirs and
# creates the files without arguments
"""def record_data():
    '''This records all the permissions data so we can remove the
    write permissions of files

    We create the files of the form:
    "file_system/file_system_data/<step_number>_<challenge_number>"
    e.g. "file_system/file_system_data/1_3"
    '''

    story_dirs = []

    # For the directories directly inside the challenge dir
    # these are the seaparate step dirs
    for step_dir in next(os.walk(FILE_SYSTEM_PATH))[1]:
        step_path = os.path.join(FILE_SYSTEM_PATH, step_dir)
        print 'step_dir = {}'.format(step_dir)
        if step_dir == 'file_system_data':
            print 'step_dir = FILE_SYSTEM_PATH'
            pass
        else:
            print 'step_dir = {}'.format(step_dir)
            for dir_path, dirs, files in os.walk(step_path):
                print "dir_path={}, dirs={}, files={}".format(dir_path, dirs, files)
                for d in dirs:
                    story_dirs.append(d)

    print 'story_dirs = {}'.format(story_dirs)

    for story_dir in story_dirs:
        pfile = os.path.join(FILE_SYSTEM_DATA_PATH, story_dir)
        file_system = os.path.join(FILE_SYSTEM_PATH, story_dir)

        with open(pfile, 'w+') as f:
            for dir_path, dirs, files in os.walk(file_system):
                for fi in files:
                    cmd = "ls -l " + os.path.join(dir_path, fi)
                    p = subprocess.check_output(cmd, shell=True)

                    # So this works in a virtual box on a Mac
                    if ".DS_Store" not in p:
                        f.write(p)
                for d in dirs:
                    cmd = "ls -ld " + os.path.join(dir_path, d)
                    p = subprocess.check_output(cmd, shell=True)

                    # So this works in a virtual box on a Mac
                    if ".DS_Store" not in p:
                        f.write(p)"""


"""def get_new_permissions(permission_list):
    groups = [permission_list[1:4], permission_list[4:7], permission_list[7:]]
    permission_array = []

    for group in groups:
        result = ""
        for char in group:
            if not char == "-":
                result = result + "1"
            else:
                result = result + "0"
        result = str(int(result, 2))
        permission_array.append(result)

    new_permissions = "".join(permission_array)
    return new_permissions


def change_permissions(permission_list, rel_path, real_loc):
    debugger("change_permissions entered")

    if not rel_path:
        return

    new_permission = get_new_permissions(permission_list)
    debugger("new_permission = {}".format(new_permission))
    cmd = ["chmod", new_permission, rel_path]
    change_permissions = subprocess.Popen(cmd,
                                          cwd=real_loc,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
    stdout, stderr = change_permissions.communicate()
    if stderr:
        debugger("Exiting change_permissions, stderr = {}".format(stderr))
        sys.exit("chmod did not work")


def change_ownership(file_owner, group_owner, rel_path, real_loc):
    debugger("change_ownership entered")

    if not rel_path:
        return

    user = get_current_user()
    new_file_owner = ""
    new_group_owner = ""

    if file_owner == "root":
        new_file_owner = "root"
    else:
        new_file_owner = user
    if group_owner == "root":
        new_group_owner = "root"
    else:
        new_group_owner = user

    chown_arg = new_file_owner + ":" + new_group_owner
    cmd = ["chown", chown_arg, rel_path]
    change_users = subprocess.Popen(cmd,
                                    cwd=real_loc,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    stdout, stderr = change_users.communicate()
    if stderr:
        sys.exit("chown did not work")"""


"""if __name__ == "__main__":
    record_data()"""
