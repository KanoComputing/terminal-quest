#!/usr/bin/env python

#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The terminals for one of the challenges

from linux_story.Terminal import Terminal
from linux_story.commands_real import ls, shell_command
from linux_story.commands_fake import cd


# Terminal that is a template for the others in this level
class Terminal1(Terminal):
    commands = ["ls"]

    def do_ls(self, line):
        return ls(self.current_dir, self.filetree, line)

    def complete_ls(self, text, line, begidx, endidx):
        text = text.split(" ")[-1]
        return self.autocomplete_desc(text, line, "both")


class Terminal2(Terminal1):
    commands = ["ls", "cat"]

    def do_cat(self, line):
        shell_command(self.current_dir, self.filetree, line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "both")


class Terminal3(Terminal2):
    commands = ["ls", "cat", "cd"]

    def do_cd(self, line):
        dir = cd(self.current_dir, self.filetree, line)
        if dir:
            self.current_dir = dir
            self.set_prompt()

    def complete_cd(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "dirs")
