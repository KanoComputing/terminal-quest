#!/usr/bin/env python

#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The a terminal for one of the challenges


from terminal import Terminal
from ..commands_real import ls, shell_command


class Terminal1(Terminal):
    def __init__(self, start_dir, end_dir, validation, hints=[""]):
        Terminal.__init__(self, start_dir, end_dir, validation, hints)

    def do_ls(self, line):
        ls(self.current_dir, self.filetree, line)

    def complete_ls(self, text, line, begidx, endidx):
        text = text.split(" ")[-1]
        return self.autocomplete_desc(text, line, "both")

    def do_cat(self, line):
        shell_command(self.current_dir, self.filetree, line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")

    def do_clear(self, line):
        shell_command(self.current_dir, self.filetree, line, "clear")
