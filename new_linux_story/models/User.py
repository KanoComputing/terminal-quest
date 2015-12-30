# User class to keep track of current position
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


class PathDoesNotExist(Exception):
    pass


class PathIsNotDir(Exception):
    pass


class User(object):
    name = os.environ["USER"]

    def __init__(self, filesystem, position):
        self._filesystem = filesystem
        position = self._test_path(position)
        self._position = position

    @property
    def filesystem(self):
        return self._filesystem

    @property
    def position(self):
        return self._position

    def set_position(self, position):
        position = self._test_path(position)
        self._position = position

    def _test_path(self, path):
        # Check path against the filesystem
        (exists, f) = self._filesystem.path_exists(path)
        if not exists:
            # This should be covered in the path_exists function
            raise PathDoesNotExist
        if not f.type == "directory":
            raise PathIsNotDir

        if path.endswith("/"):
            path = path[:-1]

        return path
