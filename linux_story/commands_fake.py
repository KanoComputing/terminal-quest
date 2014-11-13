#!/usr/bin/env python

# commands_fake.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Terminal commands which are emulated


def cd(current_dir, tree, line=None):

    if not line:
        current_dir = "~"

    else:
        folders = line.split('/')
        for f in folders:
            if f in tree.show_direct_descendents(current_dir):
                current_dir = f
            elif f == "..":
                current_dir = tree.show_ancestor(current_dir)
            # if the directory ends in a /
            elif f == "":
                pass
            else:
                # leave current prompt alone
                return False

    return current_dir
