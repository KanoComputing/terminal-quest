# commands_fake.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Terminal commands which are emulated


import os
import getpass
from kano.logging import logger

from linux_story.common import tq_file_system, fake_home_dir
from linux_story.helper_functions import debugger


def cd(real_path, line, has_access=True):
    if not has_access:
        # Could simplify this to "Permission denied"
        print "-bash: cd: {}: Permission denied".format(line)
        return

    if not line:
        new_path = fake_home_dir
    else:
        if line.startswith('~'):
            new_line = line.replace('~', fake_home_dir)
            new_path = os.path.expanduser(new_line)
        else:
            new_path = os.path.join(real_path, line)
            new_path = os.path.abspath(new_path)

        if not os.path.exists(new_path) or not os.path.isdir(new_path):
            new_path = real_path

    if new_path[-1] == '/':
        new_path = new_path[:-1]
    return new_path


# By using these python commands, we can more easily run tests on a mac.
def cat(real_path):
    with open(real_path, "r") as f:
        output = f.read()
    return output


def mkdir(real_path):
    # check if directory exists
    if os.path.exists(real_path):
        return "error", "whatever the mkdir error message is here"
    os.mkdir(real_path, 0755)
