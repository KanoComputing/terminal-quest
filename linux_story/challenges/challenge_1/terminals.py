#!/usr/bin/env python

#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The terminals for one of the challenges

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)
        print sys.path

from linux_story.Terminal import Terminal
from linux_story.commands_real import ls, shell_command


# Terminal that is a template for the others in this level
class Terminal_Template(Terminal):

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


class Terminal4(Terminal_Template):

    def check_command(self, line):
        print "entered check_command"
        if line == "ls office/filing-cabinet":
            print "predicted line correctly"
        else:
            print "incorrect preiction"
            print "line = {}".format(line)
