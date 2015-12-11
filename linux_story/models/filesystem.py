# This is only needed if we abstract away from file systems completely
import shutil
from linux_story.constants import containing_dir


class NoParentError(Exception):
    pass


class OverwritePathException(Exception):
    pass


class ChildInFileException(Exception):
    pass


class Node():
    def __init__(self, path, name, parent, permissions):
        # Full path. Maybe calculate this from the tree?
        self._path = path

        # this is the filename
        self._name = name

        # Parent directory
        self._parent = parent

        # Permissions. Useful for "ls -l" and chmod.
        self._permissions = permissions

        self._type = ""

    @property
    def parent(self):
        return self._parent

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
    def __init__(self, path, name, parent, permissions, content_file=""):
        super(FileObject, self).__init__(path, name, parent, permissions)

        self._type = "file"

        # Contents of file
        self._content = ""

        if content_file:
            self._set_content_from_file(content_file)

    @property
    def content(self):
        return self._content

    def _set_content_from_file(self, file):
        f = open(file, 'r')
        self._content = f
        f.close()


class Directory(Node):
    def __init__(self, path, name, parent, permissions, children=[]):
        super(Directory, self).__init__(path, name, parent, permissions)

        self._type = "directory"

        # Children files/directories
        self._children = children

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)


# How should the files and directory objects be structured?
class FileSystem():
    def __init__(self):
        self._tree = {}

    def add_file_at_path(self, path, name, content_file):
        tree = self._navigate_to_path()
        if tree:
            tree["name"] = name
            tree["content_file"] = content_file

    def add_dir_at_path(self, path, name):
        tree = self._navigate_to_path()
        if tree:
            tree["name"] = name
            tree["type"] = "directory"

    # Fighting the data structure?
    def get_nodes_from_path(self, path):
        tree = self._navigate_to_path()
        return tree["children"]

    def _navigate_to_path(self, path):
        levels = path.split("/")
        tree = self._tree

        # level 0 is a special case
        if tree["name"] == levels[0]:
            children = tree["children"]

        for l in levels:
            for child in children:
                if l == child["name"]:
                    tree = child
                    children = tree["children"]
                    break

        return tree


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
