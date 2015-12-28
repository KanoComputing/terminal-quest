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
        filesystem = FileSystem(self._config)
        return (filesystem, User(filesystem, position))


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
        (filesystem, user) = self._create_user("~/parent_directory/")
        self.assertEquals(user.position, "~/parent_directory")


# If filesystem tests don't work, these tests won't work
class LsInFileSystem(SetUpUser):

    def test_ls_only_1(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.do(""),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_only_2(self):
        (filesystem, user) = self._create_user("~/parent_directory/dir1")
        ls = Ls(filesystem, user)
        self.assertEquals(ls.do(""), [])

    def test_ls_with_argument_1(self):
        (filesystem, user) = self._create_user("~")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.do("parent_directory"),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_strip_trailing_slash(self):
        (filesystem, user) = self._create_user("~")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.do("parent_directory/"),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_with_argument_2(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.do("dir1"),
            []
        )

    def test_ls_with_non_existant_path(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.do("blahblah"),
            "ls: blahblah: No such file or directory"
        )

    def test_ls_tab_once_empty(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.tab_once(""),
            "ls "
        )

    def test_ls_tab_many_empty(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.tab_many(""),
            "dir1 dir2 dir3 file1 file2 file3"
        )

    def test_ls_tab_many_dirs(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.tab_many("d"),
            "dir1 dir2 dir3"
        )

    def test_ls_autocomplete_files(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.tab_many("f"),
            "file1 file2 file3"
        )

    def test_ls_tab_once_single(self):
        (filesystem, user) = self._create_user("~")
        ls = Ls(filesystem, user)
        self.assertEquals(
            ls.tab_once("parent_direct"),
            "ls parent_directory/"
        )


# If filesystem tests don't work, these tests won't work
class CdInFileSystem(SetUpUser):

    def test_cd_no_args(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        cd.do("")
        self.assertEquals(cd.position, "~")

    def test_cd_nonexistant_path_arg(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        self.assertEquals(
            cd.do("blah"),
            "cd: no such file or directory: blah"
        )

    def test_cd_no_output(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.do("dir1"), None)

    def test_cd_into_file(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.do("file1"), "bash: cd: file1: Not a directory")

    def test_cd_tab_once(self):
        (filesystem, user) = self._create_user("~")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.tab_once("pare"), "cd parent_directory/")

    def test_cd_tab_many(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.tab_many("d"), "dir1 dir2 dir3")

    def test_cd_tab_many_nested(self):
        (filesystem, user) = self._create_user("~")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.tab_many("parent_directory/d"), "dir1 dir2 dir3")

    def test_cd_go_back_output(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.do(".."), None)

    def test_cd_go_back_end_location(self):
        (filesystem, user) = self._create_user("~/parent_directory")
        cd = Cd(filesystem, user)
        cd.do("..")
        self.assertEquals(cd.position, "~")

    def test_cd_go_back_twice_output(self):
        (filesystem, user) = self._create_user("~/parent_directory/dir1")
        cd = Cd(filesystem, user)
        self.assertEquals(cd.do("../../"), None)

    def test_cd_go_back_twice_location(self):
        (filesystem, user) = self._create_user("~/parent_directory/dir1")
        cd = Cd(filesystem, user)
        cd.do("../../")
        self.assertEquals(cd.position, "~")


if __name__ == "__main__":
    unittest.main()
