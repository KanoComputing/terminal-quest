# terminal_mkdir.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.commands_real import shell_command


class TerminalMkdir(TerminalEcho):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo", "mkdir"]

    def do_mkdir(self, line):
        shell_command(self.real_path, line, "mkdir")
