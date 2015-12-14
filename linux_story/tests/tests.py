import unittest
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.models.models import Echo, Ls, Cd
from linux_story.models.User import User, PathDoesNotExist, PathIsNotDir
from linux_story.constants import command_not_found, containing_dir
from linux_story.models.filesystem import (
    make_filesystem_from_config, remove_file_system
)


class SetUpTestFileSystem(unittest.TestCase):
    filesystem = [
        {
            "name": "~",
            "type": "directory",
            "children": [
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
        }
    ]

    def _remove_old_and_set_up_filesystem(self, filesystem):
        remove_file_system()
        make_filesystem_from_config(filesystem)


class SetUpUser(SetUpTestFileSystem):
    def _create_user(self, position):
        self._remove_old_and_set_up_filesystem(self.filesystem)
        return User(position)


class CheckUser(SetUpTestFileSystem):

    def test_nonexistant_position(self):
        self._remove_old_and_set_up_filesystem(self.filesystem)
        self.assertRaises(PathDoesNotExist, User, "~/parent_directory/lalala")

    def test_file_position(self):
        self._remove_old_and_set_up_filesystem(self.filesystem)
        self.assertRaises(PathIsNotDir, User, "~/parent_directory/file1")

    def test_trailing_slash(self):
        self._remove_old_and_set_up_filesystem(self.filesystem)
        user = User("~/parent_directory/")
        self.assertEquals(user.position, "~/parent_directory")


class ModelEcho(unittest.TestCase):

    def test_echo_none(self):
        echo = Echo()
        self.assertEquals(echo.do(""), "")

    def test_echo_one(self):
        echo = Echo()
        self.assertEquals(echo.do("hello"), "hello")

    def test_greet_two(self):
        echo = Echo()
        self.assertEquals(echo.do("hello boy"), "hello boy")


# If filesystem tests don't work, these tests won't work
class LsInFileSystem(SetUpUser):

    def test_ls_only_1(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.do(""),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_only_2(self):
        user = self._create_user("~/parent_directory/dir1")
        ls = Ls(user)
        self.assertEquals(ls.do(""), [])

    def test_ls_with_argument_1(self):
        user = self._create_user("~")
        ls = Ls(user)
        self.assertEquals(
            ls.do("parent_directory"),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_strip_trailing_slash(self):
        user = self._create_user("~")
        ls = Ls(user)
        self.assertEquals(
            ls.do("parent_directory/"),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_with_argument_2(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.do("dir1"),
            []
        )

    def test_ls_with_non_existant_path(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.do("blahblah"),
            "ls: blahblah: No such file or directory"
        )

    def test_ls_tab_once_empty(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.tab_once(""),
            "ls "
        )

    def test_ls_tab_many_empty(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.tab_many(""),
            "dir1 dir2 dir3 file1 file2 file3"
        )

    def test_ls_tab_many_dirs(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.tab_many("d"),
            "dir1 dir2 dir3"
        )

    def test_ls_autocomplete_files(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.tab_many("f"),
            "file1 file2 file3"
        )

    def test_ls_tab_once_single(self):
        user = self._create_user("~")
        ls = Ls(user)
        self.assertEquals(
            ls.tab_once("parent_direct"),
            "ls parent_directory"
        )

    '''
    def test_ls_autocomplete_empty(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.autocomplete(""),
            ["dir1", "dir2", "dir3", "file1", "file2", "file3"]
        )

    def test_ls_autocomplete_dirs(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.autocomplete("d"),
            ["dir1", "dir2", "dir3"]
        )

    def test_ls_autocomplete_files(self):
        user = self._create_user("~/parent_directory")
        ls = Ls(user)
        self.assertEquals(
            ls.autocomplete("f"),
            ["file1", "file2", "file3"]
        )

    def test_ls_autocomplete_single(self):
        user = self._create_user("~")
        ls = Ls(user)
        self.assertEquals(
            ls.autocomplete("parent_direct"),
            ["parent_directory"]
        )
    '''


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

    def test_cd_tab_once(self):
        user = self._create_user("~")
        cd = Cd(user)
        self.assertEquals(cd.tab_once("pare"), "cd parent_directory")

    def test_cd_tab_many(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.tab_many("d"), "dir1 dir2 dir3")

    def test_cd_tab_many_nested(self):
        user = self._create_user("~")
        cd = Cd(user)
        self.assertEquals(cd.tab_many("parent_directory/d"), "dir1 dir2 dir3")

    '''
    def test_cd_autocomplete_dirs(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.autocomplete("d"), ["dir1", "dir2", "dir3"])

    def test_cd_autocomplete_none(self):
        user = self._create_user("~/parent_directory")
        cd = Cd(user)
        self.assertEquals(cd.autocomplete("f"), [])
    '''


if __name__ == "__main__":
    unittest.main()
