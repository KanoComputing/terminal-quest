# terminal_cat.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The a terminal for one of the challenges


from linux_story.story.terminals.terminal_ls import TerminalLs
from linux_story.commands_real import shell_command


class TerminalCat(TerminalLs):
    terminal_commands = ["ls", "cat"]

    def do_cat(self, line, has_access=True):
        if self.needs_sudo and not has_access:
            # show cat error message
            "cat: {}: Permission denied".format(line)

        shell_command(self.real_path, line, "cat")

    def complete_cat(self, text, line, begidx, endidx):
        return self.autocomplete_files(text, line, begidx, endidx)
