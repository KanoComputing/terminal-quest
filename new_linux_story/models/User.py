#!/usr/bin/env python

# User.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Simple model to represent the user, mainly to track the position of the User
# in the filesystem.


import os


class PathDoesNotExist(Exception):
    pass


class PathIsNotDir(Exception):
    pass


class User(object):
    name = os.environ["USER"]

    def __init__(self, filesystem, position):
        self._filesystem = filesystem
        position = self._test_path(position)
        self._position = position

    @property
    def filesystem(self):
        return self._filesystem

    @property
    def position(self):
        return self._position

    def set_position(self, position):
        position = self._test_path(position)
        self._position = position

    def _test_path(self, path):
        # Check path against the filesystem
        (exists, f) = self._filesystem.path_exists(path)
        if not exists:
            # This should be covered in the path_exists function
            raise PathDoesNotExist
        if not f.type == "directory":
            raise PathIsNotDir

        if path.endswith("/"):
            path = path[:-1]

        return path
