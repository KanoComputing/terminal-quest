"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Helper functions.
"""

import os
import shutil
from kano.colours import colourize256


home = os.path.expanduser("~")
hidden_dir = os.path.join(home, ".linux-story")


# copy files over from root to the home
def copy_file_tree(challenge_number):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "file-system", str(challenge_number)))

    # If path does not exist, exit function
    if not os.path.exists(path):
        return

    dest = os.path.join(os.path.expanduser("~"), ".linux-story")
    delete_file_tree()

    try:
        shutil.copytree(path, dest)
    except:
        # for now, silently fail
        # import sys
        # print "Unexpected error:", sys.exc_info()[0]
        pass


def delete_file_tree():
    filetree = os.path.join(os.path.expanduser("~"), ".linux-story")
    if os.path.exists(filetree):
        shutil.rmtree(filetree)


def is_exe(fpath):
    return os.access(fpath, os.X_OK)


def colour_file_dir(path, f):
    if os.path.isfile(path):
        if is_exe(path):
            f = colourize256(f, 118, 16, True)
        else:
            f = colourize256(f, 68, 16, True)
    elif os.path.isdir(path):
        f = colourize256(f, 29, 16, True)
    return f


def relative_loc_is_home(current_dir, tree):
    real_loc = tree[current_dir].path
    if real_loc == hidden_dir:
        return True
    return False


# This is to help the completion function in the classes
# we give this function a possible list of directories
def get_completion_dir(current_dir, tree, line):

    # list of directories
    # command will come of the form "command_name" -params directory/directory/file
    elements = line.split(" ")

    # if the last element is a load of directories (no guarentee) then we need to pick the last
    # element to maybe compare against
    dirs = elements[-1].split("/")

    direct_dirs = tree.show_direct_descendents(current_dir)
    final_list_of_dirs = []

    for d in dirs:
        if d in direct_dirs:
            final_list_of_dirs.append(d)
            direct_dirs = tree.show_direct_descendents(d)

    # return the final element
    if final_list_of_dirs:
        return final_list_of_dirs[-1]
    return current_dir
