# terminal_cat.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The a terminal for one of the challenges


from linux_story.commands_real import shell_command
from linux_story.story.terminals.terminal_ls import TerminalLs


class TerminalCat(TerminalLs):
    terminal_commands = ["ls", "cat"]

    def do_cat(self, line):
        shell_command(self._get_real_path(), line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)
