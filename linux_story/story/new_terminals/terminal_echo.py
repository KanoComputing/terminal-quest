# terminal_echo.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


from linux_story.commands_real import launch_application
from linux_story.story.new_terminals.terminal_mv import TerminalMv


class TerminalEcho(TerminalMv):
    terminal_commands = ["ls", "cat", "cd", "mv", "echo"]

    def do_echo(self, line):
        launch_application(self._location.get_real_path(), line, "echo")
