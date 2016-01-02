import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from new_linux_story.common import content_dir
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
        # start off filesystem with ~
        self._home = Directory("~", "~", [], 0755, os.environ["USER"],
                               start_challenge=-1, start_step=-1,
                               end_challenge=-1, end_step=-1)
        self.make_filesystem_from_config(config)

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
        ftype = "files", "dirs" or "all"
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
        return self.get_names_at_path(path, "all")

    def get_filenames_at_path(self, path):
        return self.get_names_at_path(path, "files")

    def get_dirnames_at_path(self, path):
        return self.get_names_at_path(path, "dirs")

    def get_files_at_path(self, path):
        all_files = self.get_all_at_path(path)
        files = [f for f in all_files if f.type == "file"]
        # Sort by name
        files = sorted(files, key=lambda k: k.name)
        return files

    def get_dirs_at_path(self, path):
        all_files = self.get_all_at_path(path)
        dirs = [f for f in all_files if f.type == "directory"]
        dirs = sorted(dirs, key=lambda k: k.name)
        return dirs

    def get_permissions_of_path(self, path):
        (exists, d) = self.path_exists(path)
        if exists:
            return d.permissions

    # Fighting the data structure?
    def path_exists(self, path, challenge=None, step=None):
        '''
        :param path: file path
        :type path: string

        :returns: (if_path_exists, tree)
        :rtype: (bool, dictionary)
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

    def _get_challenge_value(self, f, key):
        if key in f:
            return f[key]
        else:
            return -1

    def make_filesystem_from_config(self, filesystem):
        '''
        Make the filesystem in memory
        '''
        # challenge and step do not change as the filesystem is changed,
        # so do not need to passinto the function as arguments
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

    def _add_file_config_to_filesystem(self, path, f):
        name = f["name"]
        permissions = 0644
        owner = os.environ["USER"]
        start_challenge = -1
        end_challenge = -1
        start_step = -1
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
