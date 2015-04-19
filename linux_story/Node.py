#!/usr/bin/env python

# Node.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Node class, used to describe each element in the Tree class

# This is the contents of the linux-story folder that contains the
# file system needed for the challenges
from linux_story.common import tq_file_system


class Node:
    def __init__(self, identifier, path="", is_dir=False, name=""):

        self.__identifier = identifier

        if name:
            self.__name = name
        else:
            self.__name = identifier

        self.__fake_path = path
        self.calculate_real_path()
        self.__children = []
        self.__parent = None
        self.__is_dir = is_dir

        # This determines whether we save the node to a file
        self.__save_to_file = True

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    @property
    def parent(self):
        return self.__parent

    @property
    def fake_path(self):
        return self.__fake_path

    @property
    def real_path(self):
        return self.__real_path

    @property
    def is_dir(self):
        return self.__is_dir

    @property
    def name(self):
        return self.__name

    @property
    def save_to_file(self):
        return self.__save_to_file

    def add_child(self, identifier):
        self.__children.append(identifier)

    def remove_child(self, identifier):
        if identifier in self.children:
            self.children.remove(identifier)

    def add_parent(self, identifier):
        self.__parent = identifier

    def remove_parent(self):
        self.__parent = None

    def calculate_real_path(self):
        self.__real_path = self.__fake_path.replace(
            '~',
            tq_file_system
        )

    def set_as_dir(self, is_dir):
        self.__is_dir = is_dir

    def add_fake_path(self, identifier):
        self.__fake_path = identifier
        self.calculate_real_path()

    def set_save_to_file(self, identifier):
        self.__save_to_file = identifier
