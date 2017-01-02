# terminal_ls.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The terminals for one of the challenges

from linux_story.Terminal import Terminal
from linux_story.commands_real import ls


# Terminal that is a template for the others in this level
class TerminalLs(Terminal):
    terminal_commands = ["ls"]

    def do_ls(self, line):
        return ls(self.real_path, line)

    def complete_ls(self, text, line, begidx, endidx):
        return self.autocomplete_files(text, line, begidx, endidx)
