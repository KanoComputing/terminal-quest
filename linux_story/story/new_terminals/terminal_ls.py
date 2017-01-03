# terminal_ls.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The terminals for one of the challenges


from linux_story.KanoCmd import KanoCmd
from linux_story.commands_real import ls


class TerminalLs(KanoCmd):
    terminal_commands = ["ls"]

    def do_ls(self, line):
        return ls(self._location.get_real_path(), line)

    def complete_ls(self, text, line, begidx, endidx):
        return self._autocomplete_files(text, line, begidx, endidx)
