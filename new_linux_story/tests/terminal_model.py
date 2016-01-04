#!/usr/bin/env python

# terminal_model.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Run this in a linux or OSX terminal to model the fake filesystem.
#
# Check the filesystem_tests and command_tests all pass before running this.

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from new_linux_story.models.terminal import Terminal3


if __name__ == '__main__':

    config = [
        {
            "name": "dir1",
            "type": "directory",
            "children": [
                {
                    "name": "file1",
                    "type": "file"
                },
                {
                    "name": "file2",
                    "type": "file"
                },
                {
                    "name": "dir2",
                    "type": "directory",
                    "permissions": 0000,
                    "children": [
                        {
                            "name": "file2",
                            "type": "file",
                            "content": "hello",
                            "permissions": 0000
                        }
                    ]
                },
                {
                    "name": "dir3",
                    "type": "directory",
                    "children": [
                        {
                            "name": "file2",
                            "type": "file",
                            "content": "hello"
                        }
                    ]
                }
            ]
        }
    ]
    position = "~"
    Terminal3(config, position).cmdloop()
