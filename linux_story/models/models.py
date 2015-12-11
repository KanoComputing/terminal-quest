# These are the terminal models

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.constants import command_not_found
from linux_story.models.filesystem import (
    get_all_at_path, join_path, filter_tilde, get_dirs_at_path,
    get_files_at_path
)
from linux_story.models.User import User


class CommandMissingDoFunction(Exception):
    pass


class CommandMissingAutocompleteFunction(Exception):
    pass


class CmdSingle(object):
    def __init__(self):
        self._stdin = ""
        self._stdout = ""
        self._stderr = ""

    @property
    def stdin(self):
        return self._stdin

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr


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
        [command, string] = self._parse_input(line)
        if command in self._commands:
            return self._commands[command].do(string)
        else:
            return command_not_found

    def autocomplete(self, line):
        [command, string] = self._parse_input(line)
        if command in self._commands:
            return self._commands[command].autocomplete(string)
        else:
            return ""

    def _parse_input(self, line):
        words = line.split(" ")
        parsed_input = [words[0], line.replace(words[0], "").strip()]
        return parsed_input


class CmdBase(object):
    def __init__(self, user):
        # This isn't used at all
        self._ctrl = CmdSingle()
        # This is initialised elsewhere
        self._user = user

    @property
    def position(self):
        return self._user.position

    def set_position(self, position):
        return self._user.set_position(position)

    def do(self):
        pass

    def autocomplete(self, line):
        return []


class Echo(CmdSingle):

    def do(self, line):
        return line


class Pwd(CmdBase):

    def do(self, line):
        return self.position


class Ls(CmdBase):

    def do(self, line):
        if not line:
            return self._no_args()
        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "ls: {}: No such file or directory".format(name)

    def _no_args(self):
        return get_all_at_path(self.position)

    def _no_flags(self, name):
        path = join_path(self.position, name)

        if not os.path.exists(path):
            return self._no_such_file_message(name)
        return get_all_at_path(path)

    def autocomplete(self, line):
        return autocomplete_all(line, self.position)


class Cd(CmdBase):

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
        real_path = join_path(self.position, line)

        # TODO: add wrappers to all these "real" file functions
        if os.path.exists(real_path):
            if os.path.isdir(real_path):
                fake_path = os.path.join(self.position, line)
                self._user.set_position(fake_path)
            else:
                return self._cd_into_file(line)
        else:
            return self._no_such_file_message(line)

    def autocomplete(self, line):
        return autocomplete_dirs(line, self.position)


# Very repetitive code here
def autocomplete_all(line, current_position):
    '''
    :params line: the line typed on the command line so far
    :type line: str
    '''
    completions = []
    if not line:
        real_path = filter_tilde(current_position)
        completions = get_all_at_path(real_path)
    else:
        final_text = line.split("/")[-1]
        complete_path = line.replace(final_text, "")
        real_path = filter_tilde(
            os.path.join(
                current_position, complete_path
            )
        )
        if os.path.exists(real_path):
            files = get_all_at_path(real_path)
            for f in files:
                if f.startswith(final_text):
                    completions.append(f)

    return sorted(completions)


# Never used
def autocomplete_files(line, current_position):
    completions = []
    if not line:
        real_path = filter_tilde(current_position)
        completions = get_files_at_path(real_path)
    else:
        final_text = line.split("/")[-1]
        complete_path = line.replace(final_text, "")
        real_path = filter_tilde(
            os.path.join(
                current_position, complete_path
            )
        )
        if os.path.exists(real_path) and os.path.isfile(real_path):
            files = get_files_at_path(real_path)
            for f in files:
                if f.startswith(final_text):
                    completions.append(f)

    return sorted(completions)


def autocomplete_dirs(line, current_position):
    completions = []
    if not line:
        real_path = filter_tilde(current_position)
        completions = get_dirs_at_path(real_path)
    else:
        final_text = line.split("/")[-1]
        complete_path = line.replace(final_text, "")
        real_path = filter_tilde(
            os.path.join(
                current_position, complete_path
            )
        )
        if os.path.exists(real_path) and os.path.isdir(real_path):
            dirs = get_dirs_at_path(real_path)
            for d in dirs:
                if d.startswith(final_text):
                    completions.append(d)

    return sorted(completions)


class Cat(CmdBase):

    def do(self, line):
        if not line:
            # Not decided what to do here
            return

        return self._no_flags(line)

    def _no_such_file_message(self, name):
        return "cat: {}:no such file or directory".format(name)

    def _no_flags(self, line):
        real_path = join_path(self.position, line)

        if os.path.exists(real_path):
            f = open(real_path, 'r')
            contents = f.read()
            f.close()
            return contents
        else:
            return self._no_such_file_message(line)


class TerminalBase(object):
    def __init__(self, position):
        self._ctrl = CmdList()
        self._user = User(position)

    @property
    def position(self):
        return self._user.position

    def add_command(self, command_str, line):
        return self._ctrl.add_command(command_str, line)

    def receive_command(self, line):
        return self._ctrl.receive_command(line)


class Terminal1(TerminalBase):
    def __init__(self, position):
        super(Terminal1, self).__init_(position)
        self.add_command("ls", Ls(self._user))


class TerminalAll(TerminalBase):
    def __init__(self, position):
        super(TerminalAll, self).__init__(position)
        self.add_command("ls", Ls(self._user))
        self.add_command("cd", Cd(self._user))
        self.add_command("pwd", Pwd(self._user))
        self.add_command("echo", Echo())
