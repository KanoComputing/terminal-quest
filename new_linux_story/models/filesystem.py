import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


import shutil
from new_linux_story.constants import containing_dir


class NoParentError(Exception):
    pass


class OverwritePathException(Exception):
    pass


class ChildInFileException(Exception):
    pass


class CannotNavigateToPathException(Exception):
    pass


class FirstPathElementMismatchException(Exception):
    pass


class NonUniqueDirectoryException(Exception):
    pass


class PathDoesNotExistException(Exception):
    pass


class NoPathException(Exception):
    pass


class FileSystemTypeMissing(Exception):
    pass


class FileSystem(object):
    '''
    This is the filesystem in memory
    '''

    def __init__(self, filesystem):
        # start off filesystem with ~
        self._system = Directory("~", "~", 0755, [])
        self._filesystem = filesystem
        self.make_filesystem_from_config(self._filesystem)

    def add_file_at_path_with_content_file(self, path, name, content_file,
                                           permissions=0644):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(FileObject(path, name, content_file, permissions))
            return True

        return False

    def add_file_at_path_with_content(self, path, name, content,
                                      permissions=0644):
        '''
        Returns True if successfully added file to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            # Check directory permissions
            d.add_child(FileObject(path, name, content, permissions))
            return True

        return False

    def add_dir_at_path(self, path, name, permissions=0755):
        '''
        Returns True if successfully added dir to filesystem, False otherwise
        '''
        (exists, d) = self.path_exists(path)

        if exists and d.type == "directory":
            d.add_child(Directory(path, name, permissions, []))
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
    def path_exists(self, path):
        '''
        :param path: file path
        :type path: string

        :returns: (if_path_exists, tree)
        :rtype: (bool, dictionary)
        '''
        if not path:
            raise NoPathException
        # Strip the empty elements
        levels = path.split("/")
        levels = filter(None, levels)
        f = self._system

        # the first level must be ~
        if not f.name == levels[0]:
            return (False, None)

        if len(levels) == 1:
            return (True, f)

        levels = levels[1:]

        for n in range(len(levels)):
            matching_elements = [child for child in f.children
                                 if child.name == levels[n]]
            # filesystem has not been written correctly
            # TODO: Does this check need to be here?
            if len(matching_elements) > 1:
                raise NonUniqueDirectoryException
            elif len(matching_elements) == 0:
                # Path does not exist
                return (False, None)
            else:
                f = matching_elements[0]

                if n < len(levels) - 1:
                    # TODO: Maybe this check shouldn't be here
                    if not f.type == "directory":
                        raise ChildInFileException

        return (True, f)

    def make_filesystem_from_config(self, filesystem):
        '''
        Make the filesystem in memory
        '''
        def recursive_bit(path, filesystem):
            for f in filesystem:
                name = f["name"]
                objtype = f["type"]

                if objtype == "file":
                    if "children" in f:
                        raise ChildInFileException

                    if "content_file" in f:
                        content_file = f["content_file"]
                        self.add_file_at_path_from_file(path,
                                                        name,
                                                        content_file)
                    elif "content" in f:
                        content = f["content"]
                        self.add_file_at_path_with_content(path, name, content)
                    else:
                        self.add_file_at_path_with_content(path, name, "")

                elif objtype == "directory":
                    self.add_dir_at_path(path, name)

                    if "children" in f:
                        children = f["children"]
                        path = os.path.join(path, name)
                        recursive_bit(path, children)

        recursive_bit("~", filesystem)


# These work as functions as they are stored on system.
# However if we have the filesystem in memory, maybe it should be a class.
############################################################################
# Linux Filesystem:
# Update both the info and the actual filesystem
# However, do you then need this at all?
# If we continue to use ls and other commands we way we are, then yes
class LinuxFilesystem(object):
    '''
    This is how we currently actualise the filesystem on Kano OS
    '''
    containing_dir = os.path.expanduser("~/.linux-story")

    def __init__(self):
        self._filesystem = FileSystem()

    @staticmethod
    def remove_file_system():
        if os.path.exists(LinuxFilesystem.containing_dir):
            shutil.rmtree(LinuxFilesystem.containing_dir)

    @staticmethod
    def _join_path(path, name):
        path = LinuxFilesystem._filter_tilde(path)
        goal_path = os.path.join(path, name)
        return goal_path

    @staticmethod
    def _filter_tilde(path):
        if path.startswith("~"):
            path = path.replace("~", containing_dir)
            if not os.path.exists(containing_dir):
                os.mkdir(containing_dir)

        return path

    def add_file_at_path_with_content(self, path, name, content):
        self._filesystem.add_file_at_path_with_content(path, name, content)
        goal_path = self._join_path(path, name)
        f = open(goal_path, "w+")
        f.write(content)
        f.close()

    def add_file_at_path_from_file(self, path, name, content_file):
        f = open(content_file, "r")
        content = f.read()
        f.close()
        self.add_file_at_path_with_content(path, name, content)

    def add_dir_at_path(self, path, name):
        self._filesystem.add_dir_at_path(path, name)
        goal_path = self._join_path(path, name)
        if not os.path.exists(goal_path):
            os.mkdir(goal_path)

    def make_filesystem_from_config(self):

        def recursive_bit(path, filesystem):
            for f in filesystem:
                name = f["name"]
                objtype = f["type"]

                if objtype == "file":
                    if "children" in f:
                        raise ChildInFileException

                    if "content_file" in f:
                        content_file = f["content_file"]
                        self.add_file_at_path_from_file(path,
                                                        name,
                                                        content_file)
                    elif "content" in f:
                        content = f["content"]
                        self.add_file_at_path_with_content(path, name, content)
                    else:
                        self.add_file_at_path_with_content(path, name, "")

                elif objtype == "directory":
                    self.add_dir_at_path(path, name)

                    if "children" in f:
                        children = f["children"]
                        path = os.path.join(path, name)
                        recursive_bit(path, children)

        recursive_bit("~", self._filesystem)


##############################################################################
# TODO: Include these later?


class Node(object):
    def __init__(self, path, name, permissions):
        # Full path. Maybe calculate this from the tree?
        self._path = path

        # this is the filename
        self._name = name

        # Parent directory
        # self._parent = parent

        # Permissions. Useful for "ls -l" and chmod.
        self._permissions = permissions

        self._type = ""

    # @property
    # def parent(self):
    #   return self._parent

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def permissions(self):
        return self._permissions

    @property
    def type(self):
        return self._type


class FileObject(Node):
    def __init__(self, path, name, permissions, content):
        super(FileObject, self).__init__(path, name, permissions)

        self._type = "file"

        # Contents of file
        self._content = ""

    @property
    def content(self):
        return self._content

    def _set_content_from_file(self, file):
        f = open(file, 'r')
        self._content = f
        f.close()


class Directory(Node):
    def __init__(self, path, name, permissions, children):
        super(Directory, self).__init__(path, name, permissions)

        self._type = "directory"

        # Children files/directories
        self._children = children

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

'''
import os


def filter_tilde(path):
    if path.startswith("~"):
        path = path.replace("~", containing_dir)
        if not os.path.exists(containing_dir):
            os.mkdir(containing_dir)

    return path


def get_all_at_path(path):
    path = filter_tilde(path)
    return sorted(os.listdir(path))


def get_files_at_path(path):
    all_files = get_all_at_path(path)
    files = [f for f in all_files
             if os.path.isfile(os.path.join(path, f))]
    return sorted(files)


def get_dirs_at_path(path):
    all_files = get_all_at_path(path)
    dirs = [d for d in all_files
            if os.path.isdir(os.path.join(path, d))]
    return sorted(dirs)


def create_file_at_path(path, filename, content):
    goal_path = join_path(path, filename)
    f = open(goal_path, "w+")
    f.write(content)
    f.close()


def create_file_at_path_from_file(path, filename, content_file):
    f = open(content_file, "r")
    content = f.read()
    f.close()
    create_file_at_path(path, filename, content)


def create_directory_at_path(path, dirname):
    goal_path = join_path(path, dirname)
    if not os.path.exists(goal_path):
        os.mkdir(goal_path)


def join_path(path, name):
    path = filter_tilde(path)
    goal_path = os.path.join(path, name)
    return goal_path


def make_filesystem_from_config(filesystem):

    def recursive_bit(path, filesystem):
        for f in filesystem:
            name = f["name"]
            objtype = f["type"]

            if objtype == "file":
                if "children" in f:
                    raise ChildInFileException

                if "content_file" in f:
                    content_file = f["content_file"]
                    create_file_at_path_from_file(path, name, content_file)
                elif "content" in f:
                    content = f["content"]
                    create_file_at_path(path, name, content)
                else:
                    create_file_at_path(path, name, "")

            elif objtype == "directory":
                create_directory_at_path(path, name)

                if "children" in f:
                    children = f["children"]
                    path = os.path.join(path, name)
                    recursive_bit(path, children)

    recursive_bit("", filesystem)


def remove_file_system():
    if os.path.exists(containing_dir):
        shutil.rmtree(containing_dir)
'''
