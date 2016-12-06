import os
import shutil
import unittest
import sys
from mockito import *

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)
print sys.path

from linux_story.common import tq_file_system
from linux_story.story.terminals.terminal_ls import TerminalLs


class TestStringMethods(unittest.TestCase):
    """
    These tests only work on a linux (maybe unix?) filesystem, as it is reliant on running ls as a shell command.
    """
    __moved_fs = os.path.join(os.path.expanduser("~/.linux-story-moved"))

    def setUp(self):
        # Set up directory structure
        self.__setup_test_directory()
        self.terminal = TerminalLs()

    def tearDown(self):
        self.__remove_test_directory()

    def test_ls_by_itself(self):
        # need to set up a directory
        self.terminal.do_ls()
        self.assertEqual("dir1", self.terminal.do_ls())

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def __setup_test_directory(self):
        path = tq_file_system
        if os.path.exists(path):
            shutil.move(path, self.__moved_fs)
        os.makedirs(tq_file_system)
        os.mkdir(os.path.join(tq_file_system, "dir1"))
        open(os.path.join(tq_file_system, "dir1", "file1"), "w+")

    def __remove_test_directory(self):
        os.rmdir(tq_file_system)
        if os.path.exists(self.__moved_fs):
            shutil.move(self.__moved_fs, tq_file_system)


if __name__ == '__main__':
    unittest.main()