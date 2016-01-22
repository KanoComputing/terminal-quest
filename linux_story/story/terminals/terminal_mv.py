# terminal_mv.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.commands_real import shell_command


class TerminalMv(TerminalCd):
    terminal_commands = ["ls", "cat", "cd", "mv"]

    def do_mv(self, line):
        shell_command(self.real_path, line, "mv")

    def complete_mv(self, text, line, begidx, endidx):
        completions = self.autocomplete_files(text, line, begidx, endidx)
        return completions
