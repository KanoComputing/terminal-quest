#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A terminal for one of the challenges

from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.commands_real import launch_application


class TerminalEcho(TerminalMv):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo"]

    def do_echo(self, line):
        launch_application(self.real_path, line, "echo")
