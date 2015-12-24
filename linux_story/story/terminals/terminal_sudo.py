#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from linux_story.story.terminals.terminal_rm import TerminalRm
from linux_story.commands_fake import sudo


class TerminalSudo(TerminalRm):
    terminal_commands = [
        "ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm", "sudo"
    ]

    def do_sudo(self, line):
        command = line.split(" ")[0]
        following_line = "".join(line.split(" ")[1:])

        if command in self.terminal_commands:
            success_cb = getattr(self, 'do_{}'.format(command))

        sudo(self.real_path, line, 0, success_cb, following_line)


if __name__ == "__main__":
    TerminalSudo()
