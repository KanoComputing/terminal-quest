#!/usr/bin/env python

#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The a terminal for one of the challenges

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.challenges.challenge_2.terminals import TerminalCat
from linux_story.commands_fake import cd


class TerminalCd(TerminalCat):
    commands = ["ls", "cat", "cd"]

    def do_cd(self, line):
        dir = cd(self.current_dir, self.filetree, line)
        if dir:
            self.current_dir = dir
            self.set_prompt()

    def complete_cd(self, text, line, begidx, endidx):
        return self.autocomplete_desc(text, line, "dirs")
