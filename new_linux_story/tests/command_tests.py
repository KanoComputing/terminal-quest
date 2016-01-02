import unittest
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from new_linux_story.models.filesystem import FileSystem
from new_linux_story.models.User import User, PathDoesNotExist, PathIsNotDir
from new_linux_story.models.models import Ls, Cd


class SetUpUser(unittest.TestCase):
    _config = [
        {
            "name": "parent_directory",
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
                    "name": "file3",
                    "type": "file"
                },
                {
                    "name": "dir1",
                    "type": "directory"
                },
                {
                    "name": "dir2",
                    "type": "directory"
                },
                {
                    "name": "dir3",
                    "type": "directory"
                }
            ]
        }
    ]

    def _create_user(self, position):
        return User(FileSystem(self._config), position)


class CheckUser(SetUpUser):

    def test_nonexistant_position(self):
        filesystem = FileSystem(self._config)
        # TODO: these exceptions shouldn't be raised in the User class
        self.assertRaises(PathDoesNotExist,
                          User,
                          filesystem,
                          "~/parent_directory/lalala")

    def test_file_position(self):
        filesystem = FileSystem(self._config)
        self.assertRaises(PathIsNotDir,
                          User,
                          filesystem,
                          "~/parent_directory/file1")

    def test_trailing_slash(self):
        user = self._create_user("~/parent_directory/")
        self.assertEquals(user.position, "~/parent_directory")


# If filesystem tests don't work, these tests won't work
class LsInFileSystem(SetUpUser):

    def test_ls_only_1(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        files = ls.do("")["files"]
        self.assertEquals(
            sorted(f.name for f in files),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_only_2(self):
        user = self._create_user("~/parent_directory/dir1")
        ls = Ls(user)
        files = ls.do("")["files"]
        self.assertEquals([f.name for f in files], [])

    def test_ls_with_argument_1(self):
        user = self._create_user("~")
        ls = Ls(user)
        files = ls.do("parent_directory")["files"]
        self.assertEquals(
            sorted(f.name for f in files),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_strip_trailing_slash(self):
        user = self._create_user("~")
        ls = Ls(user)
        files = ls.do("parent_directory/")["files"]
        self.assertEquals(
            sorted(f.name for f in files),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_with_argument_2(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        files = ls.do("dir1")["files"]
        self.assertEquals(
            files,
            []
        )

    def test_ls_with_non_existant_path(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        message = ls.do("blahblah")["message"]
        self.assertEquals(
            message,
            "ls: blahblah: No such file or directory"
        )

    def test_ls_without_read_permission(self):
        config = [
            {
                "name": "parent_directory",
                "type": "directory",
                "owner": "root",
                "permissions": 0440,
                "children": [
                    {
                        "name": "file1",
                        "type": "file"
                    }
                ]
            }
        ]
        user = User(FileSystem(config), "~")
        ls = Ls(user)
        message = ls.do("parent_directory")["message"]
        self.assertEquals(
            message,
            "ls: parent_directory: Permission denied"
        )


# If filesystem tests don't work, these tests won't work
class CdInFileSystem(SetUpUser):

    def test_cd_no_args(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        cd.do("")
        self.assertEquals(cd.position, "~")

    def test_cd_nonexistant_path_arg(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(
            cd.do("blah"),
            "cd: no such file or directory: blah"
        )

    def test_cd_no_output(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.do("dir1"), None)

    def test_cd_into_file(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.do("file1"), "bash: cd: file1: Not a directory")

    def test_cd_go_back_output(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.do(".."), None)

    def test_cd_go_back_end_location(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        cd.do("..")
        self.assertEquals(cd.position, "~")

    def test_cd_go_back_twice_output(self):
        user = self._create_user("~/parent_directory/dir1")
        cd = Cd(user)
        self.assertEquals(cd.do("../../"), None)

    def test_cd_go_back_twice_location(self):
        user = self._create_user("~/parent_directory/dir1")
        cd = Cd(user)
        cd.do("../../")
        self.assertEquals(cd.position, "~")


if __name__ == "__main__":
    unittest.main()
