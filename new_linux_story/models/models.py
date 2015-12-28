# These are the terminal models

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from new_linux_story.constants import command_not_found
from new_linux_story.models.filesystem import FileSystem
from new_linux_story.models.User import User
from linux_story.helper_functions import colour_string_with_preset


class CommandMissingDoFunction(Exception):
    pass


class CommandMissingAutocompleteFunction(Exception):
    pass


class CmdList(object):
    def __init__(self):
        # Merge these into one data structure?
        self._commands = {}

    def add_command(self, command_str, cls):
        self._commands[command_str] = cls

        # Check this has a "do" method, otherwise raise an exception
        # Possibly also check it has an autocomplete option, otherwise have
        # a default option of returning empty.
        do = getattr(cls, "do")
        autocomplete = getattr(cls, "autocomplete")
        if not (do and callable(do)):
            raise CommandMissingDoFunction
        elif not (autocomplete and callable(autocomplete)):
            raise CommandMissingAutocompleteFunction

    def receive_command(self, line):
        '''
        Take the line from the terminal and return the output the terminal
        would show.
        '''
        [command, string] = self._parse_input(line)
        if command in self._commands:
            return self._commands[command].do(string)
        else:
            return command_not_found

    def tab_once(self, line):
        '''
        If autocomplete returns a string, then there was only one option.
        If autocomplete returns an array, then there are many options.
        '''
        [command, string] = self._parse_input(line)
        if command in self._commands:
            return self._commands[command].tab_once(string)
        else:
            return ""

    def tab_many(self, line):
        '''
        If autocomplete returns a string, then there was only one option.
        If autocomplete returns an array, then there are many options.
        '''
        [command, string] = self._parse_input(line)
        if command in self._commands:
            return self._commands[command].tab_many(string)
        else:
            return ""

    def _parse_input(self, line):
        '''
        Returns the command word and the rest of the line.
        '''
        words = line.split(" ")
        parsed_input = [words[0], line.replace(words[0], "").strip()]
        return parsed_input


class CmdSingle(object):

    def __init__(self, user=None):
        # This is initialised elsewhere
        self._user = user

    @property
    def filesystem(self):
        return self._user.filesystem

    @property
    def position(self):
        return self._user.position

    def set_position(self, position):
        return self._user.set_position(position)

    def do(self):
        pass

    def autocomplete(self, line):
        return []


# This is not
class Echo(CmdSingle):

    def do(self, line):
        return line


class Pwd(CmdSingle):

    def do(self, line):
        return self.position


class Ls(CmdSingle):

    def do(self, line):
        if not line:
            return self._no_args()
        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "ls: {}: No such file or directory".format(name)

    def _no_args(self):
        return self.filesystem.get_all_names_at_path(self.position)

    def _no_flags(self, name):
        path = os.path.join(self.position, name)
        (exists, f) = self.filesystem.path_exists(path)
        if not exists:
            return self._no_such_file_message(name)
        return self.filesystem.get_all_names_at_path(path)

    def tab_once(self, line):
        '''
        This returns the text the terminal outputs on one tab
        '''
        return tab_once("ls", line, self.position, self.filesystem, "all")

    def tab_many(self, line):
        '''
        This returns the text the terminal outputs on two tabs
        '''
        return tab_many("ls", line, self.position, self.filesystem, "all")


class Cd(CmdSingle):

    def do(self, line):
        if not line:
            return self._no_args()

        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "cd: no such file or directory: {}".format(name)

    def _cd_into_file(self, name):
        return "bash: cd: {}: Not a directory".format(name)

    def _no_args(self):
        self.set_position("~")

    def _no_flags(self, line):
        path = os.path.normpath(os.path.join(self.position, line))
        (exists, f) = self.filesystem.path_exists(path)
        if exists:
            if f.type == "directory":
                self._user.set_position(path)
            else:
                return self._cd_into_file(line)
        else:
            return self._no_such_file_message(line)

    def tab_once(self, line):
        '''
        This returns the text the terminal outputs on one tab
        '''
        return tab_once("cd", line, self.position, self.filesystem, "dirs")

    def tab_many(self, line):
        '''
        This returns the text the terminal outputs on two tabs
        '''
        return tab_many("cd", line, self.position, self.filesystem, "dirs")


def autocomplete(line, position, filesystem, config):
    '''
    :params line: the line typed on the command line so far
    :type line: str
    :params position: path
    :type position: str
    :params filesystem: FileSystem object
    :params config: "all", "files", "dirs"
    '''
    completions = []
    if not line:
        completions = filesystem.get_names_at_path(position, config)
    else:
        final_text = line.split("/")[-1]
        complete_path = "/".join(line.split("/")[:-1])
        path = os.path.join(
            position, complete_path
        )
        exists, f = filesystem.path_exists(path)
        if exists and f.type == "directory":
            for child in f.children:
                if child.name.startswith(final_text):
                    completions.append(child.name)

    return sorted(completions)


def tab_once(command, line, position, filesystem, config):
    '''
    This returns the text the terminal outputs on one tab
    '''
    completion = ""
    completions = autocomplete(line, position, filesystem, config)

    if len(completions) == 1:
        if "/" in line:
            completion = "/".join(line.split("/")[:-1])
            completion += "/" + completions[0]
        else:
            completion = completions[0]

        path = os.path.join(position, completion)
        (exists, f) = filesystem.path_exists(path)

        if f.type == "directory":
            completion = completion + "/"

        text = command + " " + completion
    else:
        text = command + " " + completion

    return text


def tab_many(command, line, position, filesystem, config):
    '''
    This returns the text the terminal outputs on one tab
    '''
    completions = autocomplete(line, position, filesystem, config)

    if len(completions) > 1:
        return " ".join(completions)
    else:
        return ""


class Cat(CmdSingle):

    def do(self, line):
        if not line:
            # Not decided what to do here
            return

        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "cat: {}:no such file or directory".format(name)

    def _no_flags(self, line):
        path = os.path.join(self.position, line)

        (exists, f) = self.filesystem.path_exists(path)
        if exists:
            return f.content
        else:
            return self._no_such_file_message(line)


class TerminalBase(object):
    def __init__(self, config, position):
        self._ctrl = CmdList()

        # TODO: move this into User
        self._user = User(FileSystem(config), position)

        # Current text shown in terminal. Not used
        self._text = ""

        self._history = []
        self._last_history = 0

    @property
    def filesystem(self):
        return self._user.filesystem

    @property
    def position(self):
        return self._user.position

    @property
    def history(self):
        return self._history

    def add_to_history(self, line):
        self.history.append(line)
        self._last_history = len(self._history)

    def go_back_in_history(self):
        if self._last_history > 0:
            self._last_history -= 1

        return self.history[self._last_history]

    def go_forward_in_history(self):
        if self._last_history < len(self.history) - 1:
            self._last_history += 1
            return self.history[self._last_history]
        else:
            self._last_history = len(self._history)
            return ""

    def add_command(self, command_str, line):
        return self._ctrl.add_command(command_str, line)

    def receive_command(self, line):
        return self._ctrl.receive_command(line)

    def tab_once(self, line):
        return self._ctrl.tab_once(line)

    def tab_many(self, line):
        return self._ctrl.tab_many(line)


class Terminal1(TerminalBase):
    def __init__(self, config, position):
        super(Terminal1, self).__init_(config, position)
        self.add_command("ls", Ls(self._user))


class TerminalAll(TerminalBase):
    def __init__(self, config, position):
        super(TerminalAll, self).__init__(config, position)
        self.add_command("ls", Ls(self._user))
        self.add_command("cd", Cd(self._user))
        self.add_command("pwd", Pwd(self._user))
        self.add_command("echo", Echo())


from cmd import Cmd


class TerminalCmd(Cmd):

    def __init__(self, config, position):
        Cmd.__init__(self)
        self._terminal = TerminalAll(config, position)

        # location of the user.
        self._prompt = ""
        self._set_prompt("~")

    @property
    def _position(self):
        return self._terminal._user.position

    def _set_prompt(self, location):

        # if prompt ends with / strip it off
        if location[-1] == '/':
            location = location[:-1]

        # Put together the terminal prompt.
        username = os.environ['LOGNAME']
        yellow_part = username + "@kano "
        yellow_part = colour_string_with_preset(yellow_part, "yellow", True)

        blue_part = location + ' $ '
        blue_part = colour_string_with_preset(blue_part, "blue", True)
        self.prompt = yellow_part + blue_part

    def do_ls(self, line):
        print self._terminal.receive_command("ls " + line)

    def do_cd(self, line):
        output = self._terminal.receive_command("cd " + line)
        if output:
            print output
        self._set_prompt(self._position)


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
    position = "~"
    TerminalCmd(config, position).cmdloop()
