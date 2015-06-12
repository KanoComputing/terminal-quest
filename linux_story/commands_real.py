#!/usr/bin/env python

# commands_real.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Terminal commands which end up running in the terminal.


import os
import subprocess

from helper_functions import colour_file_dir, debugger
from linux_story.common import tq_file_system
from kano.colours import colourize256


def ls(real_loc, line):

    new_loc = real_loc
    get_all_info = False
    new_lines = False
    args = ["ls"]
    line = line.replace('~', tq_file_system)

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
        err = err.replace(tq_file_system, '~')
        print err
        return

    # Need to filter output
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
    real_loc = tree[current_dir].real_path

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


def sudo(real_path, line):
    allowed_commands = ["chmod", "touch", "mkdir"]

    # take the list of elements
    elements = line.split(" ")

    # take the command we're sudo-ing
    command = elements[0]

    if command in allowed_commands:
        shell_command(real_path, line, "sudo")


# TODO: change this so returns differently depending on whether
# it is successful or not
def shell_command(real_loc, line, command_word=""):

    if command_word:
        line = command_word + " " + line

    line = line.replace('~', tq_file_system)

    args = line.split(" ")
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stderr:
        print stderr.strip().replace(tq_file_system, '~')
        return False

    if stdout:
        if command_word == "cat":
            print stdout
        else:
            print stdout.strip()

    # should this return stdout?
    return True


def turn_abs_path_to_real_loc(path):
    return path.replace('~', tq_file_system)


def launch_application(real_path, line, command_word=""):

    line = " ".join([command_word] + line.split(" "))

    p = subprocess.Popen(line, cwd=real_path, shell=True)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()


def nano(real_path, line):

    # File path of the local nano
    dir_path = os.path.abspath(os.path.dirname(__file__))
    nano_filepath = os.path.join(dir_path, "..", "nano-2.2.6/src/nano")

    if not os.path.exists(nano_filepath):
        # File path of installed nano
        nano_filepath = "/usr/share/linux-story/nano"

    if not os.path.exists(nano_filepath):
        raise Exception("Cannot find nano")

    cmd = nano_filepath + " " + line
    p = subprocess.Popen(cmd, cwd=real_path, shell=True)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()


def run_executable(real_path, line):

    # print "line = {}".format(line)
    line = line.strip()

    if line.startswith("./"):
        line = line[2:]

    p = subprocess.Popen(["sh", line], cwd=real_path)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()
