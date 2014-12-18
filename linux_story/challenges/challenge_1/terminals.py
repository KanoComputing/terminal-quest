#!/usr/bin/env python

#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The terminals for one of the challenges

from linux_story.Terminal import Terminal
from linux_story.commands_real import ls


# Terminal that is a template for the others in this level
class TerminalLs(Terminal):
    commands = ["ls"]

    def do_ls(self, line):
        return ls(self.current_dir, self.filetree, line)

    def complete_ls(self, text, line, begidx, endidx):
        text = text.split(" ")[-1]
        return self.autocomplete_desc(text, line, "both")
