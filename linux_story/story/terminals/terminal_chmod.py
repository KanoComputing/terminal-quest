#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.commands_real import shell_command


class TerminalChmod(TerminalNano):
    terminal_commands = [
        "ls", "cat", "cd", "mv", "echo", "mkdir", "nano", "chmod"
    ]

    def do_chmod(self, line, has_access=True):

        if self.needs_sudo and not has_access:
            print ("chmod: changing permissions of '{}': Operation not "
                   "permitted".format(line))
            return

        shell_command(self.real_path, line, "chmod")

    def complete_chmod(self, text, line, begidx, endidx):
        completions = self.autocomplete_files(text, line, begidx, endidx)
        return completions
