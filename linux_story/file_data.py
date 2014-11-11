"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Store data of filetree
* Simply records the result of 'ls -l' into a file called permissions_data
"""

import os
import subprocess
import sys
import shutil
from helper_functions import debugger


HOME = os.path.expanduser("~")
FILE_SYSTEM_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "file-system")
HIDDEN_DIR = os.path.join(HOME, ".linux-story")


def remove_username(abs_path):
    return "/".join(abs_path.split("/")[3:])


def permission_file(challenge_number=1):
    file_system_directory = os.path.join(FILE_SYSTEM_PATH, 'file_system_data')
    if not os.path.exists(file_system_directory):
        os.makedirs(file_system_directory)

    path = os.path.join(file_system_directory, str(challenge_number))

    # If path does not exist, look in lower levels
    while not os.path.exists(path):
        challenge_number = str(int(challenge_number) - 1)
        path = os.path.abspath(os.path.join(file_system_directory, challenge_number))
        debugger("path = {}".format(path))
        if challenge_number < 0:
            raise Exception("No challenges have been provided!")

    return path


def record_data(challenge_number=1):
    pfile = permission_file(challenge_number)
    with open(pfile, 'w+') as f:
        for dir_path, files, dirs in os.walk(FILE_SYSTEM_PATH):
            for d in dirs:
                cmd = "ls -l " + os.path.join(dir_path, d)
                p = subprocess.check_output(cmd, shell=True)
                f.write(p)


def copy_data(challenge_number=1):
    debugger("copy_data entered")
    copy_file_tree()
    pfile = permission_file(challenge_number)
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
            change_ownership(file_owner, group_owner, rel_path, real_loc)


# copy files over from root to the home
def copy_file_tree(challenge_number=1):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        "file-system",
                                        str(challenge_number)))

    # If path does not exist, look in lower levels
    while not os.path.exists(path):
        challenge_number = int(challenge_number) - 1
        rel_path = "file-system/" + str(challenge_number)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_path))
        if challenge_number < 0:
            raise Exception("No challenges have been provided!")

    delete_file_tree()

    try:
        shutil.copytree(path, HIDDEN_DIR)
    except:
        # for now, silently fail
        # import sys
        # print "Unexpected error:", sys.exc_info()[0]
        pass


# creates files from data file
# this doesn't currently work because we don't get the file contents
"""def create_file_tree(challenge_number=1):

    data = get_permissions_data()
    lines = data.split("\n")
    new_paths = []

    for line in lines:
        elements = lines.split(" ")
        path = elements[-1]
        dirs = path.split("/")[:8]
        new_path = "".join(dirs)
        new_paths.append(new_path)
"""


def delete_file_tree():
    filetree = os.path.join(os.path.expanduser("~"), ".linux-story")
    if os.path.exists(filetree):
        shutil.rmtree(filetree)


def generate_rel_path(abs_path):
    dirs = abs_path.split("/")[8:]
    rel_path = "/".join(dirs).strip()
    return rel_path


def get_new_permissions(permission_list):
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
        sys.exit("chown did not work")


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
        sys.exit("chown did not work")


# In bash, list users with:
# cat /etc/passwd | grep "/home" | grep "bin/bash" | cut -d: -f1
def list_users():
    cat_process = subprocess.Popen(['cat', '/etc/passwd'], stdout=subprocess.PIPE)
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


if __name__ == "__main__":
    record_data()
    copy_data()