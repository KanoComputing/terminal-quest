# User class to keep track of current position
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.models.filesystem import filter_tilde


class PathDoesNotExist(Exception):
    pass


class PathIsNotDir(Exception):
    pass


class User(object):
    def __init__(self, position):
        position = self._test_path(position)
        self._position = position

    @property
    def position(self):
        return self._position

    def set_position(self, position):
        position = self._test_path(position)
        self._position = position

    def _test_path(self, fake_path):
        real_path = filter_tilde(fake_path)
        if not os.path.exists(real_path):
            raise PathDoesNotExist
        if not os.path.isdir(real_path):
            raise PathIsNotDir

        if fake_path.endswith("/"):
            fake_path = fake_path[:-1]

        return fake_path
