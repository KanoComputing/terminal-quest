"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Helper functions.
"""

import os
import shutil
from Node import Tree
from kano.colours import colourize256, decorate_string


home = os.path.expanduser("~")
hidden_dir = os.path.join(home, ".linux-story")


# Generate from file structure
def generate_file_tree():
    tree = Tree()
    tree.add_node("~")  # root node
    tree["~"].add_path(os.path.join(os.path.expanduser("~"), ".linux-story"))

    for dirpath, dirnames, filenames in os.walk(hidden_dir):
        folders = dirpath.split("/")
        folders.remove(".linux-story")
        for d in dirnames:
            if folders[-1] == "caroline":
                tree.add_node(d, "~")
            else:
                tree.add_node(d, folders[-1])
            tree[d].add_path(os.path.join(dirpath, d))
        for f in filenames:
            if folders[-1] == "caroline":
                tree.add_node(f, "~")
            else:
                tree.add_node(f, folders[-1])
            tree[f].add_path(os.path.join(dirpath, f))
            tree[f].set_as_dir(False)

    return tree


# copy files over from root to the home
def copy_file_tree(challenge_number):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "file-system", str(challenge_number)))

    # If path does not exist, look in lower levels
    while not os.path.exists(path):
        challenge_number = int(challenge_number) - 1
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "file-system", str(challenge_number)))
        if challenge_number < 0:
            raise Exception("No challenges have been provided!")

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


# Colourise text
def get_preset_from_id(id):
    if id == 'b':
        return "light-blue"
    elif id == 'r':
        return "light-red"
    elif id == 'g':
        return "light-green"
    elif id == 'y':
        return "light-yellow"
    elif id == 'w':
        return "white"
    elif id == 'p':
        return "light-magenta"
    else:
        return "light-cyan"


def parse_string(string):
    default_preset = get_preset_from_id(None)

    if string.find("{{") == -1:
        string = decorate_string(string, default_preset)
        return string

    # First part of the string
    while string.find("{{") != -1:
        pos1 = string.index("{{")
        first_part = string[:pos1]
        # Last part of the string
        pos2 = string.index("}}")
        last_part = string[pos2 + 2:]
        # Preset id
        preset_id = string[pos1 + 2]
        preset = get_preset_from_id(preset_id)
        # Colour part of the string
        colour_part = string[pos1 + 3:pos2]
        colour_part = decorate_string(colour_part, preset)
        first_part = decorate_string(first_part, default_preset)

        if string.find("{{") != -1:
            last_part = decorate_string(last_part, default_preset)

        string = first_part + colour_part + last_part

    return string


def colourizeInput256(string, fg_num=None, bg_num=None, bold=False):
    """ Paint the text with foreground/background colours using the
        newer 256 colour model. """

    if fg_num is not None:
        string = "\001\033[38;5;%dm\002%s\001\033[0m\002" % (fg_num, string)

    if bg_num is not None:
        string = "\001\033[48;5;%dm\002%s\001\033[0m\002" % (bg_num, string)

    if bold:
        string = "\001\033[1m\002%s\001\033[0m\002" % string

    return string
