# TestFileTree.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import filecmp
import os
import shutil
import sys
import unittest

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.common import get_story_file
from linux_story.file_creation.FileTree import FileTree, revert_to_default_permissions, get_oct_permissions
from linux_story.helper_functions import is_executable


class TestFileTree(unittest.TestCase):

    def setUp(self):
        self.__end_path = os.path.expanduser("~/test-folder")

    def tearDown(self):
        revert_to_default_permissions(self.__end_path)
        if os.path.exists(self.__end_path):
            shutil.rmtree(self.__end_path)

    def test_basic_dir(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "my-house",
                    "type": FileTree.TYPE_DIR
                }
            ]
        }

        FileTree(tree, self.__end_path).parse_complete(1, 1)
        my_house = os.path.join(self.__end_path, "~/my-house")
        self.assertTrue(os.path.exists(my_house))
        self.assertTrue(os.path.isdir(my_house))

    def test_basic_file(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "Dad",
                    "contents": get_story_file("Dad"),
                    "permissions": 0755
                }
            ]
        }

        FileTree(tree, self.__end_path).parse_complete(1, 1)
        dad = os.path.join(self.__end_path, "~/Dad")
        self.assertTrue(os.path.exists(dad))
        self.assertTrue(os.path.isfile(dad))
        self.assertTrue(is_executable(dad))
        self.assertTrue(filecmp.cmp(dad, get_story_file("Dad"), shallow=False))

    def test_file_exists_challenge_1(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "Dad",
                    "contents": get_story_file("Dad"),
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1
                        },
                        {
                            "challenge": 2,
                            "step": 1,
                            "exists": False
                        }
                    ],
                }
            ]
        }
        FileTree(tree, self.__end_path).parse_complete(1, 1)
        dad = os.path.join(self.__end_path, "~/Dad")
        self.assertTrue(os.path.exists(dad))
        self.assertTrue(os.path.isfile(dad))

    def test_file_does_not_exist_challenge_2(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "Dad",
                    "contents": get_story_file("Dad"),
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1
                        },
                        {
                            "challenge": 2,
                            "step": 1,
                            "exists": False
                        }
                    ],
                }
            ]
        }

        FileTree(tree, self.__end_path).parse_complete(2, 2)
        dad = os.path.join(self.__end_path, "~/Dad")
        self.assertFalse(os.path.exists(dad))

    def test_can_create_dir_with_no_write_permission_with_child(self):
        self.__containing_folder_with_permission_removed(0500, '0500')

    def test_dir_with_no_execute_permissions_contains_child(self):
        self.__containing_folder_with_permission_removed(0600, '0600')

    def test_dir_with_no_read_permissions_contains_child(self):
        self.__containing_folder_with_permission_removed(0300, '0300')

    def test_dir_with_no_permissions_contains_child(self):
        self.__containing_folder_with_permission_removed(0000, '0')

    def __containing_folder_with_permission_removed(self, permissions, string_permissions):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "my-house",
                    "type": FileTree.TYPE_DIR,
                    "permissions": permissions,
                    "children": [
                        {
                            "name": "Dad",
                            "contents": get_story_file("Dad")
                        }
                    ]
                }
            ]
        }
        FileTree(tree, self.__end_path).parse_complete(1, 1)
        house = os.path.join(self.__end_path, "~/my-house")
        dad = os.path.join(house, "Dad")
        self.assertEquals(get_oct_permissions(house), string_permissions)
        os.chmod(house, 0755)
        self.assertTrue(os.path.exists(dad))

    def test_containing_folder_outside_challenge_scope_then_children_are(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "my-house",
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1,
                            "exists": False
                        },
                        {
                            "challenge": 2,
                            "step": 1
                        }
                    ],
                    "children": [
                        {
                            "name": "Dad",
                            "contents": get_story_file("Dad")
                        }
                    ]
                }
            ]
        }
        FileTree(tree, self.__end_path).parse_complete(1, 9)
        house = os.path.join(self.__end_path, "~/my-house")
        dad = os.path.join(house, "Dad")
        self.assertFalse(os.path.exists(house))
        self.assertFalse(os.path.exists(dad))

    def test_create_a_new_standalone_item(self):
        file_tree = FileTree(None, self.__end_path)
        contents_path = "/tmp/test"
        contents = "hello"
        open(contents_path, "w+").write(contents)
        file_tree.create_item("file", "~/my-house", 0644, contents_path)
        house = os.path.join(self.__end_path, "~/my-house")
        self.assertTrue(os.path.exists(house))
        test_contents = open(house).readline()
        self.assertEquals(contents, test_contents)

    def test_setting_permissions_in_challenges_works(self):
        tree = {
            "name": "~",
            "children": [
                {
                    "name": "my-house",
                    "type": "directory",
                    "challenges": [
                        {
                            "challenge": 1,
                            "step": 1,
                            "permissions": 0500
                        },
                        {
                            "challenge": 2,
                            "step": 1,
                            "permissions": 0300
                        }
                    ]
                }
            ]
        }
        FileTree(tree, self.__end_path).parse_complete(1, 9)
        house = os.path.join(self.__end_path, "~/my-house")
        self.assertTrue(os.path.exists(house))
        self.assertEquals(get_oct_permissions(house), "0500")
        self.tearDown()
        FileTree(tree, self.__end_path).parse_complete(2, 1)
        self.assertTrue(os.path.exists(house))
        self.assertEquals(get_oct_permissions(house), "0300")


if __name__ == '__main__':
    unittest.main()