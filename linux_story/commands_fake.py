# commands_fake.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Terminal commands which are emulated


import os


def cd(real_path, line):
    tq_file_system = os.path.join(os.path.expanduser('~'), '.linux-story')

    if not line:
        new_path = tq_file_system
    else:
        if line.startswith('~'):
            new_line = line.replace('~', '~/.linux-story')
            new_path = os.path.expanduser(new_line)
        else:
            new_path = os.path.join(real_path, line)

            # We use os.path.abspath so we don't get paths
            # like ~/my-house/../my-house
            new_path = os.path.abspath(new_path)

        if not os.path.exists(new_path) or not os.path.isdir(new_path):
            new_path = real_path

    if new_path[-1] == '/':
        new_path = new_path[:-1]
    return new_path
