#!/usr/bin/env python

# commands_real.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Terminal commands which end up running in the terminal.


import os
import subprocess

from helper_functions import colour_file_dir, debugger, hidden_dir
from kano.colours import colourize256


# We edit this to colourise the output - otherwise, we could just use shell_command
# TODO: ls -d .* doesn't work
def ls(current_dir, tree, line=""):

    # find current_location
    real_loc = tree[current_dir].path

    # Don't print anything
    if not real_loc:
        return

    new_loc = real_loc
    get_all_info = False
    new_lines = False
    args = ["ls"]
    line = line.replace('~', hidden_dir)

    if line:
        args = line.split(" ")

        for a in args:
            # flags
            if a.startswith('-'):
                # break back up into new lines
                # long format
                if a.find("l") != -1:
                    get_all_info = True
                    pass
                if a.find("1") != -1:
                    new_lines = True
                    pass
            # directory
            else:
                new_loc = os.path.join(new_loc, a)

        args = ["ls"] + args

    debugger("args = {}".format(args))
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    orig_output, err = p.communicate()
    debugger("orig_output = {}".format(orig_output))
    debugger("err = {}".format(err))

    # The error will need to be edited if it contains info about the edited
    # filename
    if err:
        err = err.replace(hidden_dir, '~')
        print err
        return

    # need to folter output
    files = orig_output.split('\n')
    coloured_files = []
    coloured_output = ""
    output = " ".join(files)

    if get_all_info:
        for f in files:
            info = f.split(" ")
            i = info[-1]
            info.pop()
            path = os.path.join(new_loc, i)
            info.append(colour_file_dir(path, i))
            f = " ".join(info)
            coloured_files.append(f)
        coloured_output = "\n".join(coloured_files)

    else:
        for f in files:
            path = os.path.join(new_loc, f)
            coloured_files.append(colour_file_dir(path, f))

        if new_lines:
            coloured_output = "\n".join(coloured_files)
        else:
            coloured_output = " ".join(coloured_files)

    print coloured_output
    return output


def grep(current_dir, tree, line):
    # find current_location
    real_loc = tree[current_dir].path

    # Don't print anything
    if not real_loc:
        return

    line = "grep " + line
    coloured_output = []
    args = line.split(" ")
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stderr:
        print stderr

    if stdout:
        results = stdout.split("/n")
        for r in results:
            [path, contents] = r.split(":")
            path = colourize256(path, 29, None, True)
            contents = colourize256(contents, 68, None, True)
            colon = colourize256(":", 118, None, True)
            coloured_output.append(colon.join([path, contents]))
        coloured_results = "/n".join(coloured_output)
        print coloured_results


def sudo(current_dir, tree, line):
    allowed_commands = ["chmod", "touch", "mkdir"]

    # take the list of elements
    elements = line.split(" ")

    # take the command we're sudo-ing
    command = elements[0]

    if command in allowed_commands:
        shell_command(current_dir, tree, line, "sudo")


# TODO: change this so returns differently depending on whether
# it is successful or not
def shell_command(current_dir, tree, line, command_word=""):

    line = " ".join([command_word] + line.split(" "))

    real_loc = tree[current_dir].path

    # Don't do anything
    if not real_loc:
        return False

    possible_path = line.split(' ')[-1]

    # TODO: very lazy.  Change
    # If path starts with ~, replace ~ with the hidden dir
    if possible_path.startswith('~'):
        possible_path = turn_abs_path_to_real_loc(possible_path)
        array = line.split(' ')[:-1]
        array.append(possible_path)
        line = ' '.join(array)

    args = line.split(" ")
    print 'real_loc = {}'.format(real_loc)
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stderr:
        print stderr.strip()
        return False

    if stdout:
        if command_word == "cat":
            print stdout
        else:
            print stdout.strip()

    # should this return stdout?
    return True


def turn_abs_path_to_real_loc(path):
    return path.replace('~', hidden_dir)


# This checks if the path is valid
def check_real_loc(tree, path):
    '''Takes a path with ~ and checks the path is consistent with the
    saved file structure.
    If so, replaces the ~ with the hidden_dir path (~/.linux-story) and
    returns the path.
    '''
    folders = path.split('/')

    # if user starts line with ~, take their path as an absolute path
    if folders[0] == '~':

        # Need to check that the path is valid
        # Check the subsequent folder do indeed belong to the correct
        # folders
        for i in range(1, len(folders)):
            if not folders[i] in tree.show_dirs(folders[i - 1]):
                return None

    path = path.replace('~', hidden_dir)
    return path


# Will be identical to touch
def mkdir(current_dir, tree, line):
    # TODO: determine if this is successful
    if shell_command(current_dir, tree, line, "mkdir"):
        real_loc = tree[current_dir].path
        args = line.split(" ")
        filepath = args[-1]

        # Hopefully we're left with the filepath
        new_dir = os.path.join(real_loc, filepath)

        # If new path was created successfully
        if os.path.exists(new_dir):
            dirs = [current_dir] + filepath.split("/")

            # Add new nodes to tree
            for i in range(len(dirs)):
                if not tree.node_exists(dirs[i]):
                    tree.add_node(dirs[i], dirs[i - 1])


def launch_application(current_dir, tree, line, command_word=""):

    line = " ".join([command_word] + line.split(" "))

    real_loc = tree[current_dir].path

    # Don't do anything
    if not real_loc:
        return

    p = subprocess.Popen(line, cwd=real_loc, shell=True)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()
