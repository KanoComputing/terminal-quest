#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The terminals for one of the challenges

from linux_story.Terminal import Terminal
from linux_story.commands_real import ls


# Terminal that is a template for the others in this level
class TerminalLs(Terminal):
    terminal_commands = ["ls"]

    def do_ls(self, line):
        # this is so we can read the output of the command for
        # self.output_command
        return ls(self.real_path, line)

    def complete_ls(self, text, line, begidx, endidx):
        return self.autocomplete_files(text, line, begidx, endidx)
