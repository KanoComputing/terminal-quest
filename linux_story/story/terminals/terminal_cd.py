#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The a terminal for one of the challenges

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cat import (
    TerminalCat
)

from linux_story.commands_fake import cd


class TerminalCd(TerminalCat):
    commands = ["ls", "cat", "cd"]

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


if __name__ == "__main__":
    start_path = '~'
    end_path = '~/my-house'

    def check_command(arg1=None, arg2=None):
        pass

    def block_command(arg1=None, arg2=None):
        pass

    def check_output(arg1=None, arg2=None):
        pass

    terminal = TerminalCd(
        start_path,
        end_path,
        check_command,
        block_command,
        check_output
    )

    terminal.cmdloop()
