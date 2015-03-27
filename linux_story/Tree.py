#!/usr/bin/env python

# Tree.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v

#
# Emulate file system in a tree class


import os
import sys
import yaml
import shutil

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from linux_story.helper_functions import parse_string

from linux_story.Node import Node
from linux_story.get_defaults import get_default_file_dict

# This is the path to the filesystem on the system
from linux_story.common import CONTENT_FOLDER, TREE_HOME, TREE_SNAPSHOT

# TODO: this is repeated!!
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))


(_ROOT, _DEPTH, _BREADTH) = range(3)

# Global variable
story_filetree = None


def load_global_tree():
    '''This loads the filetree from the save file in the system
    '''

    global story_filetree

    story_filetree = StoryFileTree()
    success = story_filetree.load_tree()

    # if successful, exit
    if success == 0:
        return


def default_global_tree(challenge, step):
    '''This creates the filetree from the yaml of challenge 1
    '''

    global story_filetree

    story_filetree = StoryFileTree()
    story_dict = get_default_file_dict(challenge, step)

    return story_filetree.modify_file_tree(story_dict)


class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):

        # if the node already exists, just return it
        if self.node_exists(identifier):
            return self[identifier]

        # Otherwise, just create it
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self.add_parent_to_identifier(identifier, parent)

        return node

    def add_parent_to_identifier(self, identifier, parent):
        '''This adds the parent to the identifier, and also
        makes the node the child of the parent.
        This way we can easily traverse around the tree.
        '''

        if identifier not in self[parent].children:
            self[parent].add_child(identifier)
            self[parent].set_as_dir(True)
        self[identifier].add_parent(parent)

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

    def show_files_or_dirs(self, identifier, list_type):
        '''Show the files or directories depending on list_type variable
        list_type is one of "both", "files" or "dirs"
        '''

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
        # In kano-toolset, but for now want to avoid dependencies
        username = os.environ['LOGNAME']
        prompt = current_dir + ' $ '
        for node in self.show_all_ancestors(current_dir):
            prompt = node + "/" + prompt
        prompt = "{{Y" + username + "@kano " + "}}" + "{{b" + prompt + "}}"
        # return prompt

        coloured_prompt = parse_string(prompt, input=True)
        return coloured_prompt


###########################################################
# These are functions to control and save the Tree class

class StoryFileTree(Tree):

    def create_item(self, dest_path, item_type="file", src_path=""):
        '''Create a file or directory
        Parameters:
        dest_path: a string of the destination path
        item_type: "file" or "directory"
        src_path: a string of the source path
        '''
        if not os.path.exists(dest_path):
            if item_type == 'file':
                shutil.copyfile(src_path, dest_path)
            elif item_type == 'directory':
                os.mkdir(dest_path)

    def delete_item(self, path):
        '''Delete the file or directory specified by path.
        '''
        if os.path.exists(path):
            if os.path.isdir():
                shutil.rmtree(path)
            else:
                os.remove(path)

    # TODO: This could be done better.
    def split_path_and_add_dirs_to_tree(self, item_id):
        '''This breaks up the path of the item_id and adds all
        the containing directories to the tree, if they haven't been added
        already
        '''

        fake_path = self[item_id].fake_path
        dirs = fake_path.split('/')

        for i in range(len(dirs) - 1):
            # directory name is the tree ID?
            # This is slightly inconsistent with the tree ID system
            # where the keys are decided from the yaml
            if not self.node_exists(dirs[i]):

                # Get the path of the directory from the path
                dir_path = fake_path.split(dirs[i])[0] + dirs[i]
                self.add_node(dirs[i])
                self[dirs[i]].set_as_dir(True)
                self[dirs[i]].add_fake_path(dir_path)

                # Create the directory in the file system
                real_path = self[dirs[i]].real_path
                self.create_item(real_path, item_type="directory")

            # If the index of the array is not 0, and the node of the
            # tree does not have a parent, then add the parent as the
            # previous directory
            if i != 0 and not self[dirs[i]].parent:
                self.add_parent_to_identifier(dirs[i], dirs[i - 1])

    # TODO this is a MONSTER function.
    # Break it up.
    def modify_file_tree(self, filesystem_dict):
        '''This modifies the tree in memory and the filesystem the user
        interacts with. It also stores the tree as a yaml, which is saved on
        Kano World
        '''

        containing_dir = os.path.dirname(os.path.abspath(__file__))

        # Move this to the common.py?
        containing_dir_of_files = os.path.join(
            containing_dir, "ascii_assets"
        )

        for item_names, item_dict in filesystem_dict.iteritems():
            item_ids = item_names.split(', ')
            for item_id in item_ids:

                # Check if the item is specified to exist
                if 'exists' in item_dict.keys() and not item_dict['exists']:
                    # This only works when the node is in the tree.
                    # However, if it isn't, then it shouldn't exist anyway
                    if self.node_exists(item_id):
                        self.delete_item(self[item_id].real_path)
                        self.remove_node(item_id)

                    # Go to the next item_id
                    continue

                # This is here to stop a node being overwriteen should it
                # already exist.
                # This may be an unnecessary condition as there is a condition
                # in add_node which may be enough.
                elif not self.node_exists(item_id):
                    self.add_node(item_id)

                # If 'path' is in the item dictionary, then make sure the
                # relevent directory or file exists in the right place
                if 'path' in item_dict.keys():

                    # Check also if "name" is in the dictionary, as this will
                    # change the name of the filepath.
                    if 'name' in item_dict.keys():

                        fake_path = os.path.join(
                            item_dict['path'], item_dict['name']
                        )

                    else:
                        fake_path = os.path.join(item_dict['path'], item_id)

                    self[item_id].add_fake_path(fake_path)

                    # Changes tree
                    self.split_path_and_add_dirs_to_tree(item_id)

                # Copy the file contents in the file system
                path_to_file_in_system = os.path.join(
                    containing_dir_of_files,
                    item_id
                )

                # Check if the item is a directory.
                # By default, assume is a file

                if 'directory' in item_dict.keys():
                    # When converting from python to yaml and back to python,
                    # booleans go from True to true
                    # is_dir = item_dict['directory'].lower() == "true"
                    self[item_id].set_as_dir(item_dict['directory'])

                    # Create the directory in the file system
                    if item_dict['directory']:
                        self.create_item(self[item_id].real_path, "directory")
                    else:
                        self.create_item(
                            self[item_id].real_path,
                            item_type="file",
                            src_path=path_to_file_in_system
                        )

                else:
                    # print 'entering create_item'
                    # print 'item_id = {}'.format(item_id)
                    # print 'self[item_id] = {}'.format(self[item_id])
                    self.create_item(
                        self[item_id].real_path,
                        item_type="file",
                        src_path=path_to_file_in_system
                    )

                if 'parent' in item_dict.keys():
                    self.add_parent_to_identifier(item_id, item_dict['parent'])

    def save_tree(self):
        '''This saves the filesystem as a yaml, which is then stored in
        Terminal-Quest-content.
        '''

        file_dict = {}

        nodes = self.nodes

        for item_id, node in nodes.iteritems():
            nodename = node.fake_path.split('/')[-1]
            nodepath = '/'.join(node.fake_path.split('/')[:-1])

            file_dict[item_id] = {}

            if nodepath:
                file_dict[item_id]["path"] = nodepath

            file_dict[item_id]["name"] = nodename
            file_dict[item_id]["directory"] = node.is_dir

        yaml_data = yaml.dump(file_dict)

        if not os.path.exists(CONTENT_FOLDER):
            os.mkdir(CONTENT_FOLDER)

        f = open(TREE_SNAPSHOT, 'w+')
        f.write(yaml_data)
        f.close()

    def load_tree(self):
        '''This loads the tree from the yaml and creates it at linux-story
        (Is this the best way?)
        This returns 1 if unsuccessful, 0 otherwise
        '''

        if os.path.exists(TREE_SNAPSHOT):
            f = open(TREE_SNAPSHOT)
            yaml_data = f.read()
            f.close()

            file_data_dict = yaml.load(yaml_data)
            if os.path.exists(TREE_HOME):
                shutil.rmtree(TREE_HOME)

            self.modify_file_tree(file_data_dict)
            # If successful, return 1
            return 0

        # If it fails, return 1
        return 1


if __name__ == "__main__":

    tree = StoryFileTree()
    tree.load_tree()
