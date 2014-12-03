#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Class which shows the contents of hints and storyline files in tmp

import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from file_functions import file_exists, read_file, delete_file


class StoryUi():
    def __init__(self):
        self.file_exists("story")
        self.read_file("story")

    def file_exists(self, file_name):
        exists = file_exists(file_name)
        if exists:
            print "{} exists = {}".format(file_name, file_exists(file_name))
        return file_exists(file_name)

    def read_file(self, file_name):
        if self.file_exists(file_name):
            file_contents = read_file(file_name)
            print "{} contents = {}".format(file_name, file_contents)
            delete_file(file_name)
