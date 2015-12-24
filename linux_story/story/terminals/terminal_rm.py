#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.commands_real import shell_command


class TerminalRm(TerminalChmod):
    terminal_commands = [
        "ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm"
    ]

    def do_rm(self, line, has_access=True):
        shell_command(self.real_path, line, "rm")

    def complete_rm(self, text, line, begidx, endidx):
        completions = self.autocomplete_files(text, line, begidx, endidx)
        return completions
