#!/usr/bin/env python

# filesystem.py
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Contains classes that model a Linux filesystem.


import os
from new_linux_story.common import content_dir, username
from new_linux_story.models.files import Directory, FileObject


class PathDoesNotExistException(Exception):
    pass


class FileSystemTypeMissing(Exception):
    pass


class NoPathException(Exception):
    pass


class NonUniqueFileException(Exception):
    pass


class ChildInFileException(Exception):
    pass


class FileSystem(object):
    '''
    This is the filesystem in memory
    '''

    def __init__(self, config):
        # Start off filesystem with ~, owned by user that should exist for all
        # challenges
        self._home = Directory("~", "~", [], 0755, username,
                               start_challenge=1, start_step=1,
                               end_challenge=-1, end_step=-1)
        self.make_filesystem_from_config(config)

    def make_filesystem_from_config(self, filesystem):
        '''
        Make the filesystem in memory.
        '''
        # challenge and step do not change as the filesystem is changed,
        # so do not need to pass into the function as arguments
        def recursive_bit(path, filesystem):
            for f in filesystem:
                name = f["name"]
                objtype = f["type"]

                if objtype == "file":
                    self._add_file_config_to_filesystem(path, f)

                elif objtype == "directory":
                    self._add_dir_config_to_filesystem(path, f)

                    if "children" in f:
                        children = f["children"]
                        recursive_bit(os.path.join(path, name), children)

        recursive_bit("~", filesystem)

    def add_file_at_path_from_file(self, path, name, content_file,
                                   permissions, owner, start_c,
                                   start_s, end_s, end_c):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            content = ""
            with open(content_file, 'r') as f:
                content = f.read()

            d.add_child(FileObject(path, name, content, permissions,
                                   owner, start_c, start_s, end_s, end_c))
            return True

        return False

    def add_file_at_path_with_content(self, path, name, content,
                                      permissions, owner, start_c,
                                      start_s, end_s, end_c):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(FileObject(path, name, content, permissions,
                                   owner, start_c, start_s, end_s, end_c))
            return True

        return False

    def add_dir_at_path(self, path, name, permissions, owner, start_c,
                        start_s, end_s, end_c):
        '''
        Returns True if successfully added dir to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(Directory(path, name, [], permissions, owner,
                                  start_c, start_s, end_s, end_c))
            return True

        return False

    def get_all_at_path(self, path):
        (exists, d) = self.path_exists(path)

        if not exists:
            raise PathDoesNotExistException

        if exists and d.type == "directory":
            return sorted(d.children, key=lambda k: k.name)

    def get_names_at_path(self, path, ftype):
        '''
        Given the path of the containing directory, get the names of the files,
        or directories, or both.
        :param path: path of the containing directory
        :type path: string
        :param ftype: "files", "dirs" or "all"
        :type ftype: string
        :returns: the names in the containing directory.
        :rtype: list of strings
        '''

        if ftype == "all":
            files = self.get_all_at_path(path)
        elif ftype == "files":
            files = self.get_files_at_path(path)
        elif ftype == "dirs":
            files = self.get_dirs_at_path(path)
        else:
            raise FileSystemTypeMissing

        names = []
        # This should preserve the order
        for f in files:
            names.append(f.name)
        return names

    def get_all_names_at_path(self, path):
        '''
        Given the path of the containing directory, get the names of all the
        files and directories.
        :param path: path of the containing directory
        :type path: string
        :return: names of all the files and directories in the
                 containing directory
        :rtype: list of strings
        '''
        return self.get_names_at_path(path, "all")

    def get_filenames_at_path(self, path):
        '''
        Given the path of the containing directory, get the names of only the
        files.
        :param path: path of the containing directory
        :type path: string
        :return: names of only the files in the containing directory
        :rtype: list of strings
        '''
        return self.get_names_at_path(path, "files")

    def get_dirnames_at_path(self, path):
        '''
        Given the path of the containing directory, get the names of only the
        directories.
        :param path: path of the containing directory
        :type path: string
        :return: names of only the directories in the containing directory
        :rtype: list of strings
        '''
        return self.get_names_at_path(path, "dirs")

    def get_files_at_path(self, path):
        '''
        :param path: path of the containing directory
        :type path: string
        :returns: the objects representing the files located at that path.
        :rtype: list of FileObject instances
        '''
        all_files = self.get_all_at_path(path)
        files = [f for f in all_files if f.type == "file"]
        # Sort by name
        files = sorted(files, key=lambda k: k.name)
        return files

    def get_dirs_at_path(self, path):
        '''
        :param path: path of the containing directory
        :type path: string
        :returns: the list objects representing the directories located at
                  that path.
        :rtype: list of Directory objects
        '''
        all_files = self.get_all_at_path(path)
        dirs = [f for f in all_files if f.type == "directory"]
        dirs = sorted(dirs, key=lambda k: k.name)
        return dirs

    def get_permissions_of_path(self, path):
        '''
        Find the permission of the Directory or the FileObject located at the
        path.
        :param path: path of the file or directory you want to know the
                     permissions of
        :type path: string
        :returns: the permissions of that object
        :rtype: int
        '''
        (exists, d) = self.path_exists(path)
        if exists:
            return d.permissions

    # Fighting the data structure?
    def path_exists(self, path, challenge=None, step=None):
        '''
        Check if the path exists in the filesystem.
        If a challenge and step are not provided, then this function will
        check if the path exists at some point, but there is no information
        for which challenges.

        :param path: file path you want to check exists
        :type path: string
        :param challenge: challenge which you want to check
        :type challenge: int or None
        :param step: step number where the file should exist
        :type step: int or None
        :returns: tuple saying if the path exists, and the FileObject or
                  Directory that exists with that path.
        :rtype: (bool if_path_exists, FileObject or Directory instance)
        '''
        if not path:
            raise NoPathException

        # Remove .. and redundant slashes
        path = os.path.normpath(path)

        # Strip the empty elements
        levels = path.split("/")
        levels = filter(None, levels)
        f = self._home

        # the first level must be ~
        if not f.name == levels[0]:
            return (False, None)

        if len(levels) == 1:
            return (True, f)

        levels = levels[1:]

        for n in range(len(levels)):
            matching_elements = [child for child in f.children
                                 if child.name == levels[n]]
            # TODO: Does this check need to be here?
            if len(matching_elements) > 1:
                raise NonUniqueFileException
            elif len(matching_elements) == 0:
                # Path does not exist
                return (False, None)
            else:
                f = matching_elements[0]

                if n < len(levels) - 1:
                    # TODO: Maybe this check shouldn't be here
                    if not f.type == "directory":
                        raise ChildInFileException

        if challenge and step:
            if f.exists_in_challenge(challenge, step):
                return (True, f)
            else:
                return (False, None)

        return (True, f)

    def _add_file_config_to_filesystem(self, path, f):
        '''
        Add a file represented by a dictionary
        :param path: path to the file
        :type path: string
        :param f: dictionary representing the file, with keys:
                  name, permissions, owner, start_challenge, end_challenge,
                  start_step, end_step, content or content_file

        '''
        name = f["name"]

        # Default arguments
        permissions = 0644
        owner = username
        start_challenge = 1
        end_challenge = -1
        start_step = 1
        end_step = -1

        # TODO: repeated owner logic for dir and file
        if "permissions" in f:
            permissions = f["permissions"]

        if "owner" in f:
            owner = f["owner"]

        if "children" in f:
            raise ChildInFileException

        if "start_challenge" in f:
            start_challenge = f["start_challenge"]

        if "end_challenge" in f:
            end_challenge = f["end_challenge"]

        if "start_step" in f:
            start_step = f["start_step"]

        if "end_step" in f:
            end_step = f["end_step"]

        if "content_file" in f:
            content_file = f["content_file"]
            content_file = os.path.join(content_dir, content_file)
            self.add_file_at_path_from_file(path,
                                            name,
                                            content_file,
                                            permissions,
                                            owner,
                                            start_challenge,
                                            start_step,
                                            end_challenge,
                                            end_step)
        elif "content" in f:
            content = f["content"]
            self.add_file_at_path_with_content(path,
                                               name,
                                               content,
                                               permissions,
                                               owner,
                                               start_challenge,
                                               start_step,
                                               end_challenge,
                                               end_step)
        else:
            self.add_file_at_path_with_content(path,
                                               name,
                                               "",
                                               permissions,
                                               owner,
                                               start_challenge,
                                               start_step,
                                               end_challenge,
                                               end_step)

    def _add_dir_config_to_filesystem(self, path, f):
        '''
        Add a directory to the filesystem represented by a dictionary

        :param path: path to the directory
        :type path: string
        :param f: dictionary representing the directory, with keys:
                  name, permissions, owner, start_challenge, end_challenge,
                  start_step, end_step

        '''
        name = f["name"]
        permissions = 0755
        owner = os.environ["USER"]
        start_challenge = -1
        end_challenge = -1
        start_step = -1
        end_step = -1

        if "permissions" in f:
            permissions = f["permissions"]

        if "owner" in f:
            owner = f["owner"]

        if "start_challenge" in f:
            start_challenge = f["start_challenge"]

        if "end_challenge" in f:
            end_challenge = f["end_challenge"]

        if "start_step" in f:
            start_step = f["start_step"]

        if "end_step" in f:
            end_step = f["end_step"]

        self.add_dir_at_path(path, name, permissions, owner,
                             start_challenge, start_step, end_challenge,
                             end_step)
