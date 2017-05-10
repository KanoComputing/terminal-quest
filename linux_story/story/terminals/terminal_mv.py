# terminal_mv.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


from linux_story.commands_real import shell_command, launch_application
from linux_story.story.terminals.terminal_cd import TerminalCd


class TerminalMv(TerminalCd):
    terminal_commands = ["ls", "cat", "cd", "mv"]

    def do_mv(self, line):
        if "*" in line:
            launch_application(self._location.get_real_path(), line, "mv")
        else:
            shell_command(self._location.get_real_path(), line, "mv")

    def complete_mv(self, text, line, begidx, endidx):
        completions = self._autocomplete_files(text, line, begidx, endidx)
        return completions
