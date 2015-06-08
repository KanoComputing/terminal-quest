#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The a terminal for one of the challenges

from linux_story.story.terminals.terminal_cat import (
    TerminalCat
)

from linux_story.commands_fake import cd


class TerminalCd(TerminalCat):
    terminal_commands = ["ls", "cat", "cd"]

    def do_cd(self, line):
        new_path = cd(self.real_path, line)
        if new_path:
            self.real_path = new_path
            self.generate_fake_path()
            self.set_prompt()

    def complete_cd(self, text, line, begidx, endidx):
        try:
            return self.autocomplete_files(text, line, begidx, endidx, only_dirs=True)
        except Exception as e:
            print str(e)
