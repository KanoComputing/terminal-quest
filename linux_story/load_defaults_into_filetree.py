
import os
import shutil

from kano.logging import logger
from linux_story.get_defaults import get_default_file_dict
from linux_story.common import (tq_backup_folder, tq_file_system,
                                get_tq_backup_tree_path,
                                create_tq_backup_tree_path)


def default_global_tree(challenge, step):
    '''This creates the filetree from the yaml of challenge 1
    '''

    # If we are loading from the default file system, we
    # don't want to pollute it with anything lingering
    if os.path.exists(tq_file_system):
        shutil.rmtree(tq_file_system)

    story_dict = get_default_file_dict(challenge, step)

    modify_file_tree(story_dict)


def load_tree(challenge, step):
    '''This uncompresses the file and copies it to the correct
    directory
    '''
    pass


def create_item(dest_path, item_type="file", src_path=""):
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


def delete_item(path):
    '''Delete the file or directory specified by path.
    '''
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


# TODO: This could be done better.
def split_path_and_add_dirs_to_tree(item_id, fake_path):
    '''This breaks up the path of the item_id and adds all
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


# TODO this is a MONSTER function.
# Break it up.
# TODO: if we modifiy apple path, when autocompleting we still see where
# the old apple was.
def modify_file_tree(filesystem_dict):
    '''This modifies the tree in memory and the filesystem the user
    interacts with. It also stores the tree as a yaml, which is saved on
    Kano World
    '''

    if not os.path.exists(tq_file_system):
        os.mkdir(tq_file_system)

    containing_dir = os.path.dirname(os.path.abspath(__file__))

    # Move this to the common.py?
    containing_dir_of_files = os.path.join(
        containing_dir, "ascii_assets/story_files"
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
                if 'directory' in item_dict.keys():
                    # Create the directory in the file system
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

                else:
                    create_item(
                        real_path,
                        item_type="file",
                        src_path=path_to_file_in_system
                    )


def save_tree(challenge, step):
    '''This saves the filesystem as a yaml, which is then stored in
    Terminal-Quest-content.
    It needs to be a yaml so we can store meta information about the
    filesystem, like whether the files are readable and writable
    '''
    pass
