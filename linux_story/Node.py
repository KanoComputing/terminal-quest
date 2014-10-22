"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Emulate file system in a tree class
"""

import os

# TODO: this is repeated!!
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))


(_ROOT, _DEPTH, _BREADTH) = range(3)


class Node:
    def __init__(self, identifier, path="", is_dir=True):
        self.__identifier = identifier
        self.__path = path
        self.__children = []
        self.__parent = None
        self.__is_dir = is_dir

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
    def path(self):
        return self.__path

    @property
    def is_dir(self):
        return self.__is_dir

    def add_child(self, identifier):
        self.__children.append(identifier)

    def add_parent(self, identifier):
        self.__parent = identifier

    def add_path(self, identifier):
        self.__path = identifier

    def set_as_dir(self, is_dir):
        self.__is_dir = is_dir


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
        return hasattr(self, identifier)

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item

    def generate_prompt(self, current_dir):
        prompt = current_dir + '$ '
        for node in self.show_all_ancestors(current_dir):
            prompt = node + "/" + prompt
        prompt = "user@kano:" + prompt
        return prompt
