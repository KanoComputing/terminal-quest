# terminal_ls.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The terminals for one of the challenges


import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

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
