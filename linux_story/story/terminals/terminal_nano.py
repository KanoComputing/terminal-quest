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

import threading

from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.commands_real import nano


class TerminalNano(TerminalEcho):
    commands = ["ls", "cat", "cd", "mv", "echo", "mkdir", "nano"]

    def do_nano(self, line):
        self.set_nano_running(True)

        # Read nano in a separate thread
        t = threading.Thread(target=self.get_nano_contents)
        t.daemon = True
        t.start()

        nano(self.real_path, line)
