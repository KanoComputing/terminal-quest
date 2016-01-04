#!/usr/bin/env python

# common.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Place to store common constants.


import os


command_not_found = "command not found"
containing_dir = os.path.expanduser("~/.linux-story")

content_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "content")
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
story_data = os.path.join(data_dir, "filesystem.json")
username = os.environ["USER"]
