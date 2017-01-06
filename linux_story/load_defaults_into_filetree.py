# load_defaults_into_filetree.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This takes the file tree from the yaml and creates it.


import os
import shutil
import stat

from linux_story.get_defaults import get_default_file_dict
from linux_story.common import tq_file_system, fake_home_dir
from linux_story.helper_functions import get_path_to_file_in_system


def default_global_tree(challenge, step):
    """
    This creates the filetree from the yaml of challenge 1
    """
    print "old style"

    # If we are loading from the default file system, we
    # don't want to pollute it with anything lingering
    if os.path.exists(tq_file_system):
        revert_to_default_permissions()
        shutil.rmtree(tq_file_system)

    story_dict = get_default_file_dict(challenge, step)

    modify_file_tree(story_dict)


def create_item(dest_path, item_type="file", src_path="", item_perm=None):
    """
    Create a file or directory
    Args:
        dest_path (str): the destination path
        item_type (str): "file" or "directory"
        src_path (str): the source path
    """

    # if item_perm is None:
    #     if item_type == "file":
    #         item_perm = 0644
    #     else:
    #         item_perm = 0755


    if os.path.exists(dest_path) and item_perm is not None:
        permissions = int(stat.S_IMODE(os.stat(dest_path).st_mode))
        if not permissions == item_perm:
            os.chmod(dest_path, item_perm)

    elif not os.path.exists(dest_path):
        permissions_changed = False

        # Check permissions of the parent directory
        parent_dir = os.path.normpath(os.path.join(dest_path, ".."))
        mode = os.stat(parent_dir).st_mode
        parent_permissions = int(stat.S_IMODE(mode))

        # Lazy - just checking owner has write permissions
        # if len(permissions) < 3 or int(permissions[-3]) % 4 < 2:
        if not bool(mode & stat.S_IXUSR):
            os.chmod(parent_dir, 0755)
            permissions_changed = True


        if not bool(mode & stat.S_IWUSR):
            os.chmod(parent_dir, 0755)
            permissions_changed = True


        if item_type == 'file':
            shutil.copyfile(src_path, dest_path)
        elif item_type == 'directory':
            os.mkdir(dest_path)

        if item_perm:
            os.chmod(dest_path, item_perm)

        if permissions_changed:
            # change permissions of the parent directory back
            # print "changing parent dir " + parent_dir + " back to permissions " + str(parent_permissions)
            os.chmod(parent_dir, parent_permissions)


def delete_item(path):
    """
    Delete the file or directory specified by path.
    """

    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


# TODO: This could be done better.
def split_path_and_add_dirs_to_tree(item_id, fake_path):
    """
    This breaks up the path of the item_id and adds all
    the containing directories to the tree, if they haven't been added
    already
    """

    dirs = fake_path.split('/')

    for i in range(len(dirs) - 1):

        # Get the path of the directory from the path
        dir_path = fake_path.split(dirs[i])[0] + dirs[i]

        # Create the directory in the file system
        real_path = os.path.expanduser(dir_path.replace('~', fake_home_dir))
        create_item(real_path, item_type="directory")


def modify_file_tree(filesystem_dict):
    """
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

    """

    if not os.path.exists(tq_file_system):
        os.mkdir(tq_file_system)

    for item_names, item_dict in filesystem_dict.iteritems():

        item_ids = item_names.split(', ')
        for item_id in item_ids:

            if __file_does_not_exist(item_dict):
                continue

            # If specified, change the permissions of the file
            permissions = None
            if "permissions" in item_dict.keys():
                permissions = item_dict["permissions"]

            if 'path' in item_dict:
                if 'name' in item_dict:
                    fake_path = os.path.join(item_dict['path'], item_dict['name'])
                else:
                    fake_path = os.path.join(item_dict['path'], item_id)
                real_path = os.path.expanduser(fake_path.replace('~', fake_home_dir))
                # Changes tree
                split_path_and_add_dirs_to_tree(item_id, fake_path)

                # Get the file location in the file system
                path_to_file_in_system = get_path_to_file_in_system(item_id)

                # If the file is specified as a directory.
                if 'directory' in item_dict.keys() and item_dict['directory']:
                    create_item(
                        real_path,
                        item_type="directory",
                        item_perm=permissions
                    )
                else:
                    create_item(
                        real_path,
                        item_type="file",
                        src_path=path_to_file_in_system,
                        item_perm=permissions
                    )


def __file_does_not_exist(item_dict):
    return 'exists' in item_dict.keys() and not item_dict['exists']


# Call this on closing the application.
# TODO: Also record what the permission was before overwriting.
# TODO: abstract away from changing the permissions directly.
def revert_to_default_permissions():
    '''
    This is the brute force way of cleaning up the permissions
    We go through the tree and change ALL permissions to 666
    '''

    print "in revert to default permissions"
    for root, dirs, files in os.walk(tq_file_system):
        for d in dirs:
            path = os.path.join(root, d)
            os.chmod(path, 0755)
        for f in files:
            path = os.path.join(root, f)
            os.chmod(path, 0644)
