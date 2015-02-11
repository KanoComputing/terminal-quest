#!/usr/bin/env python

# commands_fake.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Terminal commands which are emulated


def cd(current_dir, tree, line=None):

    # if user enters 'cd' by itself, takae them to ~
    if not line:
        new_current_dir = "~"

    # Decide where to move the user
    else:
        new_current_dir = current_dir

        folders = line.split('/')

        # if user starts line with ~, take their path as an absolute path
        if folders[0] == '~':

            # Need to check that the path is valid
            # Check the subsequent folder do indeed belong to the correct
            # folders
            for i in range(1, len(folders)):
                if not folders[i] in tree.show_dirs(folders[i - 1]):
                    new_current_dir = current_dir
                    return new_current_dir

            new_current_dir = folders[-1]

        # This assumes you are moving somewhere relative to where you started
        # from
        else:
            for f in folders:
                if f in tree.show_dirs(new_current_dir):
                    new_current_dir = f
                elif f == "..":
                    new_current_dir = tree.show_ancestor(new_current_dir)

                # if the directory ends in a /
                elif f == "":
                    pass
                else:
                    new_current_dir = current_dir

    return new_current_dir
