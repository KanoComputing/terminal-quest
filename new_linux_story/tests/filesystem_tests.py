import unittest
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from new_linux_story.models.filesystem import (
    make_filesystem_from_config, remove_file_system, get_all_at_path,
    get_files_at_path, get_dirs_at_path, ChildInFileException
)
from new_linux_story.constants import containing_dir


class FilesystemTests(unittest.TestCase):

    one_dir = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "test2",
                    "type": "directory"
                }
            ]
        }
    ]

    one_file_no_content = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "test2",
                    "type": "file"
                }
            ]
        }
    ]

    one_parent_one_child = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "test",
                    "type": "directory",
                    "children": [
                        {
                            "name": "blah",
                            "type": "file"
                        }
                    ]
                }
            ]
        }
    ]

    one_parent_many_children = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "dir1",
                    "type": "directory",
                    "children": [
                        {
                            "name": "file1",
                            "type": "file"
                        },
                        {
                            "name": "file2",
                            "type": "file"
                        },
                        {
                            "name": "dir1",
                            "type": "directory"
                        },
                        {
                            "name": "dir2",
                            "type": "directory"
                        }
                    ]
                }
            ]
        }
    ]

    file_with_children = [
        {
            "name": "~",
            "type": "directory",
            "children": [
                {
                    "name": "file1",
                    "type": "file",
                    "children": [
                        {
                            "name": "file1",
                            "type": "file"
                        },
                        {
                            "name": "file2",
                            "type": "file"
                        }
                    ]
                }
            ]
        }
    ]

    def test_file_should_not_have_children(self):
        remove_file_system()
        self.assertRaises(
            ChildInFileException,
            make_filesystem_from_config,
            self.file_with_children
        )

    def test_file(self):
        '''
        Check that an empty file is created
        '''
        self._remove_old_and_set_up_filesystem(self.one_file_no_content)
        path_that_should_exist = os.path.join(containing_dir, "test2")

        # This should be abstracted away from os.path.exists
        is_file = os.path.isfile(path_that_should_exist)
        self.assertEquals(is_file, True)

    def test_directory(self):
        '''
        Check that a directory is created
        '''
        self._remove_old_and_set_up_filesystem(self.one_dir)
        path_that_should_exist = os.path.join(containing_dir, "test2")

        # This should be abstracted away from os.path.isdir
        is_dir = os.path.isdir(path_that_should_exist)
        self.assertEquals(is_dir, True)

    def test_parent_child_created(self):
        self._remove_old_and_set_up_filesystem(self.one_parent_one_child)
        path_that_should_exist = os.path.join(containing_dir, "test/blah")
        path_exists = os.path.exists(path_that_should_exist)
        self.assertEquals(path_exists, True)

    def test_list_all_children_correctly(self):
        self._remove_old_and_set_up_filesystem(self.one_parent_many_children)
        path = os.path.join(containing_dir, "dir1")
        files = get_all_at_path(path)
        self.assertEquals(files, ["dir1", "dir2", "file1", "file2"])

    def test_list_file_children_correctly(self):
        self._remove_old_and_set_up_filesystem(self.one_parent_many_children)
        path = os.path.join(containing_dir, "dir1")
        files = get_files_at_path(path)
        self.assertEquals(files, ["file1", "file2"])

    def test_list_dir_children_correctly(self):
        self._remove_old_and_set_up_filesystem(self.one_parent_many_children)
        path = os.path.join(containing_dir, "dir1")
        files = get_dirs_at_path(path)
        self.assertEquals(files, ["dir1", "dir2"])

    def _remove_old_and_set_up_filesystem(self, filesystem):
        remove_file_system()
        make_filesystem_from_config(filesystem)

if __name__ == "__main__":
    unittest.main()
