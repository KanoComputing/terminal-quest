#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A terminal for one of the challenges

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.commands_real import shell_command


class TerminalMv(TerminalCd):
    commands = ["ls", "cat", "cd", "mv"]

    def do_mv(self, line):
        shell_command(self.current_dir, self.filetree, line, "mv")
        self.update_tree()

    def complete_mv(self, text, line, begidx, endidx):
        completions = self.autocomplete_desc(text, line, "both")
        return completions
