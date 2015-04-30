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
    commands = ["ls"]

    def do_ls(self, line):
        # this is so we can read the output of the command for
        # self.output_command
        return ls(self.real_path, line)

    def complete_ls(self, text, line, begidx, endidx):
        return self.autocomplete_files(text, line, begidx, endidx)


# For testing separately
if __name__ == "__main__":

    import os
    import sys

    if __name__ == '__main__' and __package__ is None:
        dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
        if dir_path != '/usr':
            sys.path.insert(1, dir_path)

    start_path = '~'
    end_path = '~/my-house'

    def check_command(arg1=None, arg2=None):
        pass

    def block_command(arg1=None, arg2=None):
        pass

    def check_output(arg1=None, arg2=None):
        pass

    terminal = TerminalLs(
        start_path,
        end_path,
        check_command,
        block_command,
        check_output
    )

    terminal.cmdloop()
