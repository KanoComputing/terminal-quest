#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

from linux_story.commands_real import shell_command
from linux_story.story.new_terminals.terminal_chmod import TerminalChmod


class TerminalRm(TerminalChmod):
    terminal_commands = [
        "ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod", "rm"
    ]

    def do_rm(self, line):
        shell_command(self._location.get_real_path(), line, "rm")

    def complete_rm(self, text, line, begidx, endidx):
        completions = self._autocomplete_files(text, line, begidx, endidx)
        return completions
