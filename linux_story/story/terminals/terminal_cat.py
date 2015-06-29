#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The a terminal for one of the challenges

from linux_story.story.terminals.terminal_ls import TerminalLs
from linux_story.commands_real import shell_command


class TerminalCat(TerminalLs):
    terminal_commands = ["ls", "cat"]

    def do_cat(self, line):
        shell_command(self.real_path, line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self.autocomplete_files(text, line, begidx, endidx)
