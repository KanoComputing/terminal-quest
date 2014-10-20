"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Terminal commands which end up running in the terminal.
"""

import os
import subprocess
from helper_functions import colour_file_dir


def ls(loc, tree, line=""):

    # find current_location
    real_loc = tree[loc].path

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


def shell_command(current_dir, tree, line):
    real_loc = tree[current_dir].path

    # Don't do anything
    if not real_loc:
        return

    args = line.split(" ")
    p = subprocess.Popen(args, cwd=real_loc,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stdout:
        print stdout.strip()

    if stderr:
        print stderr.strip()


def launch_application(current_dir, tree, line):
    real_loc = tree[current_dir].path

    p = subprocess.Popen(line, cwd=real_loc, shell=True)
    stdout, stderr = p.communicate()

    if stderr:
        print stderr.strip()
