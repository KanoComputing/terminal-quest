import unittest
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from new_linux_story.models.filesystem import FileSystem, ChildInFileException


class SingleFileChecks(unittest.TestCase):
    one_file_no_content_one_dir = [
        {
            "name": "file1",
            "type": "file"
        },
        {
            "name": "dir1",
            "type": "directory"
        }
    ]

    def test_file_exists(self):
        '''
        Check that an empty file is created
        '''
        filesystem = FileSystem(self.one_file_no_content_one_dir)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(exists, True)

    def test_file_is_file(self):
        '''
        Check that an empty file is created
        '''
        filesystem = FileSystem(self.one_file_no_content_one_dir)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.type, "file")

    def test_dir_exists(self):
        '''
        Check that an empty file is created
        '''
        filesystem = FileSystem(self.one_file_no_content_one_dir)
        (exists, d) = filesystem.path_exists("~/dir1")
        self.assertEquals(exists, True)

    def test_dir_is_dir(self):
        '''
        Check that an empty file is created
        '''
        filesystem = FileSystem(self.one_file_no_content_one_dir)
        (exists, d) = filesystem.path_exists("~/dir1")
        self.assertEquals(d.type, "directory")


class SingleFilesAndDirs(unittest.TestCase):

    def test_file_should_not_have_children(self):
        file_with_children = [
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
        # filesystem = self._setup(file_with_children)
        self.assertRaises(
            ChildInFileException,
            FileSystem,
            file_with_children
        )

    def test_directory(self):
        '''
        Check that a directory is created
        '''
        one_dir = [
            {
                "name": "test2",
                "type": "directory"
            }
        ]
        filesystem = self._setup(one_dir)
        (exists, d) = filesystem.path_exists("~/test2")
        self.assertEquals(d.type, "directory")

    def test_parent_child_created(self):
        one_parent_one_child = [
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
        filesystem = self._setup(one_parent_one_child)
        (path_exists, d) = filesystem.path_exists("~/test/blah")
        self.assertEquals(path_exists, True)

    def _setup(self, config):
        filesystem = FileSystem(config)
        return filesystem


class ChildrenInDirectory(unittest.TestCase):
    one_parent_many_children = [
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

    def test_list_all_children_correctly(self):
        filesystem = self._setup(self.one_parent_many_children)
        [dir1, dir2, file1, file2] = filesystem.get_all_at_path("~/dir1")
        self.assertEquals([dir1.name, dir2.name, file1.name, file2.name],
                          ["dir1", "dir2", "file1", "file2"])

    def test_list_file_children_correctly(self):
        filesystem = self._setup(self.one_parent_many_children)
        [file1, file2] = filesystem.get_files_at_path("~/dir1")
        self.assertEquals([file1.name, file2.name], ["file1", "file2"])

    def test_list_dir_children_correctly(self):
        filesystem = self._setup(self.one_parent_many_children)
        [dir1, dir2] = filesystem.get_dirs_at_path("~/dir1")
        self.assertEquals([dir1.name, dir2.name], ["dir1", "dir2"])

    def _setup(self, config):
        filesystem = FileSystem(config)
        # filesystem.make_filesystem_from_config(self.one_parent_many_children)
        return filesystem


class PermissionsChecks(unittest.TestCase):
    def test_default_dir_permissions(self):
        single_directory = [
            {
                "name": "dir1",
                "type": "directory",
            }
        ]
        filesystem = FileSystem(single_directory)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.permissions, 0755)

    def test_default_file_permissions(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.permissions, 0644)

    def test_locked_dir(self):
        single_locked_directory = [
            {
                "name": "dir1",
                "type": "directory",
                "permissions": 0000
            }
        ]
        filesystem = FileSystem(single_locked_directory)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.permissions, 0000)

    def test_locked_file(self):
        single_locked_file = [
            {
                "name": "file1",
                "type": "file",
                "permissions": 0000
            }
        ]
        filesystem = FileSystem(single_locked_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.permissions, 0000)


class OwnerChecks(unittest.TestCase):
    def test_default_file_owner(self):
        single_file = [
            {
                "name": "file1",
                "type": "file"
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.owner, os.environ["USER"])

    def test_default_dir_owner(self):
        single_dir = [
            {
                "name": "dir1",
                "type": "directory"
            }
        ]
        filesystem = FileSystem(single_dir)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.owner, os.environ["USER"])

    def test_changed_dir_owner(self):
        single_dir = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "root"
            }
        ]
        filesystem = FileSystem(single_dir)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.owner, "root")

    def test_changed_file_owner(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root"
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.owner, "root")


class ReadAccess(unittest.TestCase):
    def test_read_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0444
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_read_permission("caroline"), True)

    def test_different_owner_no_read_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0440,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_read_permission("caroline"), False)

    def test_same_owner_no_read_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "caroline",
                "permissions": 0000,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_read_permission("caroline"), False)

    def test_custom_owner_read_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "caroline",
                "permissions": 0042,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_read_permission("caroline"), True)

    def test_read_access_dir(self):
        single_dir = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "root",
                "permissions": 0444
            }
        ]
        filesystem = FileSystem(single_dir)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.has_read_permission("caroline"), True)

    def test_different_owner_no_read_access_dir(self):
        single_file = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "root",
                "permissions": 0440,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.has_read_permission("caroline"), False)

    def test_same_owner_no_read_access_dir(self):
        single_file = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "caroline",
                "permissions": 0000,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.has_read_permission("caroline"), False)

    def test_custom_owner_read_access_dir(self):
        single_file = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "caroline",
                "permissions": 0042,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/dir1")
        self.assertEquals(f.has_read_permission("caroline"), True)

    def test_execute_permissions_on_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0443
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_execute_permission("caroline"), True)

    def test_custom_owner_no_execute_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0440,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_execute_permission("caroline"), False)

    def test_custom_owner_execute_access_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "caroline",
                "permissions": 0100,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_execute_permission("caroline"), True)

    def test_write_permissions_on_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0666
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_write_permission("caroline"), True)

    def test_custom_owner_no_write_permissions_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "root",
                "permissions": 0664,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_write_permission("caroline"), False)

    def test_custom_owner_write_permissions_file(self):
        single_file = [
            {
                "name": "file1",
                "type": "file",
                "owner": "caroline",
                "permissions": 0644,
            }
        ]
        filesystem = FileSystem(single_file)
        (exists, f) = filesystem.path_exists("~/file1")
        self.assertEquals(f.has_write_permission("caroline"), True)

    def test_multiple_dirs_custom_owner(self):
        directories = [
            {
                "name": "dir1",
                "type": "directory",
                "owner": "caroline"
            },
            {
                "name": "dir2",
                "type": "directory",
                "owner": "caroline"
            },
            {
                "name": "dir3",
                "type": "directory",
                "owner": "caroline"
            },
            {
                "name": "dir4",
                "type": "directory",
                "owner": "caroline"
            }
        ]
        filesystem = FileSystem(directories)
        names = filesystem.get_all_names_at_path("~")
        self.assertEquals(names, ["dir1", "dir2", "dir3", "dir4"])

    def test_content(self):
        pass

    def test_multiple_dirs_with_children(self):
        config = [
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
                        "type": "directory",
                        "children": [
                            {
                                "name": "file2",
                                "type": "file"
                            }
                        ]
                    },
                    {
                        "name": "dir2",
                        "type": "directory",
                        "children": [
                            {
                                "name": "file1",
                                "type": "file"
                            }
                        ]
                    }
                ]
            }
        ]
        filesystem = FileSystem(config)
        names = filesystem.get_all_names_at_path("~/dir1")
        self.assertEquals(names, ["dir1", "dir2", "file1", "file2"])


if __name__ == "__main__":
    unittest.main()
