from cmd import Cmd
import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from new_linux_story.models.filesystem import FileSystem
from new_linux_story.models.models import CmdList, Ls, Cd, Cat, Pwd, Echo
from new_linux_story.models.User import User
from linux_story.helper_functions import colour_string_with_preset


class TerminalAll(object):
    def __init__(self, config, position, cmd):
        self._ctrl = CmdList()
        self._user = User(FileSystem(config), position)
        self._cmd = cmd
        self.add_command("ls", Ls(self._user)),
        self.add_command("cd", Cd(self._user))
        self.add_command("cat", Cat(self._user))
        self.add_command("pwd", Pwd(self._user))
        self.add_command("echo", Echo())

    @property
    def filesystem(self):
        return self._user.filesystem

    @property
    def position(self):
        return self._user.position

    def create_prompt(self, location):

        # if prompt ends with / strip it off
        if location[-1] == '/':
            location = location[:-1]

        # Put together the terminal prompt.
        username = os.environ['LOGNAME']
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = location + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)
        return yellow_part + blue_part

    def add_command(self, command_str, line):
        return self._ctrl.add_command(command_str, line)

    def receive_command(self, line):
        return self._ctrl.receive_command(line)

    def tab_once(self, line):
        return self._ctrl.tab_once(line)

    def tab_many(self, line):
        return self._ctrl.tab_many(line)

    def autocomplete(self, line):
        return self._ctrl.autocomplete(line)

    def ls(self, line):
        output = self.receive_command("ls " + line)
        message = output["message"]
        files = output["files"]

        if message:
            print message
        else:
            coloured = []
            for f in files:
                if f.type == "directory":
                    coloured.append(
                        colour_string_with_preset(
                            f.name, "blue", True
                        )
                    )
                elif f.type == "file":
                    coloured.append(f.name)
            print " ".join(coloured)

    def complete_ls(self, line):
        return self.autocomplete(line)

    def cd(self, line):
        output = self.receive_command("cd " + line)
        if output:
            print output
        self._cmd.prompt = self.create_prompt(self.position)

    def complete_cd(self, line):
        return self.autocomplete(line)

    def cat(self, line):
        print self.receive_command("cat " + line)

    def complete_cat(self, line):
        return self.autocomplete(line)


class TerminalCmdBase(Cmd):
    def __init__(self, config, position):
        Cmd.__init__(self)
        self._terminal = TerminalAll(config, position, self)
        self.prompt = self._terminal.create_prompt(position)


class Terminal1(TerminalCmdBase):

    def do_ls(self, line):
        return self._terminal.ls(line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._terminal.complete_ls(line)


class Terminal2(TerminalCmdBase):

    def do_cd(self, line):
        return self._terminal.cd(line)

    def complete_cd(self, text, line, begidx, endidx):
        return self._terminal.complete_cd(line)


class Terminal3(TerminalCmdBase):

    def do_ls(self, line):
        return self._terminal.ls(line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._terminal.complete_ls(line)

    def do_cd(self, line):
        return self._terminal.cd(line)

    def complete_cd(self, text, line, begidx, endidx):
        return self._terminal.complete_cd(line)

    def do_cat(self, line):
        return self._terminal.cat(line)

    def complete_cat(self, text, line, begidx, endidx):
        return self._terminal.complete_cat(line)


if __name__ == '__main__':
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
                    "name": "dir2",
                    "type": "directory",
                    "permissions": 0000,
                    "children": [
                        {
                            "name": "file2",
                            "type": "file",
                            "content": "hello",
                            "permissions": 0000
                        }
                    ]
                },
                {
                    "name": "dir3",
                    "type": "directory",
                    "children": [
                        {
                            "name": "file2",
                            "type": "file",
                            "content": "hello"
                        }
                    ]
                }
            ]
        }
    ]
    position = "~"
    Terminal3(config, position).cmdloop()
