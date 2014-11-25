#!/usr/bin/env python

# Tree.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Emulate file system in a tree class


import os
from linux_story.helper_functions import hidden_dir, parse_string
from linux_story.Node import Node

# TODO: this is repeated!!
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))


(_ROOT, _DEPTH, _BREADTH) = range(3)


# With this class, files have to have unique names
class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)
            self[parent].set_as_dir(True)
            self[identifier].add_parent(parent)

        return node

    def remove_node(self, identifier):
        if hasattr(self, identifier):
            del self[identifier]

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print "{0}".format(identifier)
        else:
            print "t" * depth, "{0}".format(identifier)

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett,
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def show_direct_descendents(self, identifier):
        queue = self[identifier].children
        while queue:
            yield queue[0]
            queue = queue[1:]

    def show_visible_descendents(self, identifier):
        queue = self[identifier].children
        while queue:
            if not queue[0].startswith("."):
                yield(queue[0])
            queue = queue[1:]

    def show_files(self, identifier):
        queue = self[identifier].children
        while queue:
            if not self[queue[0]].is_dir:
                yield queue[0]
            queue = queue[1:]

    def show_dirs(self, identifier):
        queue = self[identifier].children
        while queue:
            if self[queue[0]].is_dir:
                yield queue[0]
            queue = queue[1:]

    def show_type(self, identifier, list_type):
        if list_type == "both":
            direct_descs = self.show_direct_descendents(identifier)
        elif list_type == "dirs":
            direct_descs = self.show_dirs(identifier)
        else:
            direct_descs = self.show_files(identifier)

        return direct_descs

    def show_ancestor(self, identifier):
        parent = self[identifier].parent
        return parent

    def show_all_ancestors(self, identifier):
        queue = self[identifier].parent
        while queue:
            yield queue
            expansion = self[queue].parent
            queue = expansion

    def node_exists(self, identifier):
        return identifier in self.__nodes

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def generate_prompt(self, current_dir):
        # in kano-toolset, but for now want to avoid dependencies
        username = os.environ['LOGNAME']
        prompt = current_dir + ' $ '
        for node in self.show_all_ancestors(current_dir):
            prompt = node + "/" + prompt
        prompt = "{{Y" + username + "@kano " + "}}" + "{{b" + prompt + "}}"
        coloured_prompt = parse_string(prompt, input=True)
        return coloured_prompt


# Generate from file structure
def generate_file_tree():
    # in kano-toolset, but for now want to avoid dependencies
    username = os.environ['LOGNAME']
    tree = Tree()
    tree.add_node("~")  # root node
    tree["~"].add_path(os.path.join(os.path.expanduser("~"), ".linux-story"))

    for dirpath, dirnames, filenames in os.walk(hidden_dir):
        folders = dirpath.split("/")
        folders.remove(".linux-story")

        for d in dirnames:
            if folders[-1] == username:
                tree.add_node(d, "~")
            else:
                tree.add_node(d, folders[-1])
            tree[d].add_path(os.path.join(dirpath, d))
        for f in filenames:
            if folders[-1] == username:
                tree.add_node(f, "~")
            else:
                tree.add_node(f, folders[-1])

            tree[f].add_path(os.path.join(dirpath, f))
            tree[f].set_as_dir(False)

    return tree
