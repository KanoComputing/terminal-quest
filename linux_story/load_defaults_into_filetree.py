#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# load_defaults_into_filetree.py

# This takes the file tree from the yaml and creates it.


import os
import shutil

from linux_story.get_defaults import get_default_file_dict
from linux_story.common import tq_file_system


def default_global_tree(challenge, step):
    '''
    This creates the filetree from the yaml of challenge 1
    '''

    # If we are loading from the default file system, we
    # don't want to pollute it with anything lingering
    if os.path.exists(tq_file_system):
        shutil.rmtree(tq_file_system)

    story_dict = get_default_file_dict(challenge, step)

    modify_file_tree(story_dict)


def create_item(dest_path, item_type="file", src_path=""):
    '''
    Create a file or directory
    Args:
        dest_path (str): the destination path
        item_type (str): "file" or "directory"
        src_path (str): the source path
    '''

    if not os.path.exists(dest_path):
        if item_type == 'file':
            shutil.copyfile(src_path, dest_path)
        elif item_type == 'directory':
            os.mkdir(dest_path)


def delete_item(path):
    '''
    Delete the file or directory specified by path.
    '''

    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


# TODO: This could be done better.
def split_path_and_add_dirs_to_tree(item_id, fake_path):
    '''
    This breaks up the path of the item_id and adds all
    the containing directories to the tree, if they haven't been added
    already
    '''

    dirs = fake_path.split('/')

    for i in range(len(dirs) - 1):

        # Get the path of the directory from the path
        dir_path = fake_path.split(dirs[i])[0] + dirs[i]

        # Create the directory in the file system
        real_path = os.path.expanduser(dir_path.replace('~', '~/.linux-story'))
        create_item(real_path, item_type="directory")


def modify_file_tree(filesystem_dict):
    '''
    This modifies the game filesystem.

    Args:
        filesystem_dict (dict): a dictionary of the form:
        {
            file_id: {
                "exists": bool,
                "permissions": int,
                "path": str
            }
        }

    '''

    if not os.path.exists(tq_file_system):
        os.mkdir(tq_file_system)

    containing_dir = os.path.dirname(os.path.abspath(__file__))

    # Move this to the common.py?
    containing_dir_of_files = os.path.join(
#arf
        containing_dir, "ascii_assets/story_files/it"
#arf
    )

    for item_names, item_dict in filesystem_dict.iteritems():

        item_ids = item_names.split(', ')
        for item_id in item_ids:

            # Check if the item is specified to exist
            if 'exists' in item_dict.keys() and not item_dict['exists']:
                # Go to the next item_id
                continue

            if 'path' in item_dict:
                if 'name' in item_dict:
                    fake_path = os.path.join(item_dict['path'], item_dict['name'])
                else:
                    fake_path = os.path.join(item_dict['path'], item_id)
                real_path = os.path.expanduser(fake_path.replace('~', '~/.linux-story'))
                # Changes tree
                split_path_and_add_dirs_to_tree(item_id, fake_path)

                # Copy the file contents in the file system
                path_to_file_in_system = os.path.join(
                    containing_dir_of_files,
                    item_id
                )

                # If the file is specified as a directory.
                if 'directory' in item_dict.keys():
                    # Create the directory in the file system.
                    if item_dict['directory']:
                        create_item(
                            real_path,
                            item_type="directory"
                        )
                    else:
                        create_item(
                            real_path,
                            item_type="file",
                            src_path=path_to_file_in_system
                        )
                # Default - make the item into a file.
                else:
                    create_item(
                        real_path,
                        item_type="file",
                        src_path=path_to_file_in_system
                    )

                # If specified, change the permissions of the file
                if "permissions" in item_dict.keys():
                    mode = item_dict["permissions"]
                    os.chmod(real_path, mode)


# Call this on closing the application.
# TODO: Also record what the permission was before overwriting.
def revert_to_default_permissions():
    '''
    This is the brute force way of cleaning up the permissions
    We go through the tree and change ALL permissions to 666
    '''

    for root, dirs, files in os.walk(tq_file_system):
        for d in dirs:
            path = os.path.join(root, d)
            os.chmod(path, 0755)
        for f in files:
            path = os.path.join(root, f)
            os.chmod(path, 0644)
