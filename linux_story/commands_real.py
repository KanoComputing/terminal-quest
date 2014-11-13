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
from helper_functions import colour_file_dir
from kano.colours import colourize256


# We edit this to colourise the output - otherwise, we could just use shell_command
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

    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate()

    # need to folter output
    files = output.split('\n')
    coloured_files = []

    if get_all_info:
        for f in files:
            info = f.split(" ")
            i = info[-1]
            info.pop()
            path = os.path.join(new_loc, i)
            info.append(colour_file_dir(path, i))
            f = " ".join(info)
            coloured_files.append(f)
        output = "\n".join(coloured_files)

    else:
        for f in files:
            path = os.path.join(new_loc, f)
            coloured_files.append(colour_file_dir(path, f))

        if new_lines:
            output = "\n".join(coloured_files)
        else:
            output = " ".join(coloured_files)

    print output


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


def shell_command(current_dir, tree, line, command_word=""):

    line = " ".join([command_word] + line.split(" "))

    real_loc = tree[current_dir].path

    # Don't do anything
    if not real_loc:
        return False

    args = line.split(" ")
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()

    return True


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
