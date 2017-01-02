# terminal_cd.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The a terminal for one of the challenges


import os
import stat
from linux_story.commands_fake import cd
from linux_story.step_helper_functions import route_between_paths
from linux_story.story.new_terminals.terminal_cat import TerminalCat


def not_locked(directory):
    uid = os.geteuid()
    gid = os.getegid()
    s = os.stat(directory)
    mode = s[stat.ST_MODE]
    return (
        ((s[stat.ST_UID] == uid) and (mode & stat.S_IXUSR)) or
        ((s[stat.ST_GID] == gid) and (mode & stat.S_IXGRP)) or
        (mode & stat.S_IWOTH)
    )


class TerminalCd(TerminalCat):
    terminal_commands = ["ls", "cat", "cd"]

    def do_cd(self, line):
        if self.__check_cd(line):
            self._set_command_blocked(False)
            new_path = cd(self._location.get_real_path(), line)
            if not not_locked(new_path):
                self._set_command_blocked(True)
                print (
                    _("bash: cd: " + line + ": Permission denied")
                )
            elif new_path:
                self._location.set_real_path(new_path)
                self._set_prompt()
        else:
            self._set_command_blocked(True)
            print (_("Nice try! But you entered an unexpected destination path."))

    def complete_cd(self, text, line, begidx, endidx):
        try:
            return self._autocomplete_files(text, line, begidx, endidx, only_dirs=True)
        except Exception as e:
            print str(e)

    def __check_cd(self, line):
        """If returns True, that means that cd will bring the user closer
        to their destination, so cd should be allowed to run with the
        user's choice of path.
        """

        # Get the current list of the paths that we're allowed to go on
        route = route_between_paths(self._location.get_fake_path(), self._location.get_end_dir())

        if not route and self._dirs_to_attempt:
            route = route_between_paths(self._location.get_fake_path(), self._dirs_to_attempt)

        if line:
            if line.startswith("~"):
                new_path = line
            else:
                new_path = os.path.join(self._location.get_fake_path(), line)
        else:
            # If the user didn't enter a path, assume they want to go to
            # home folder
            new_path = '~'

        new_path = os.path.abspath(os.path.expanduser(new_path))
        if new_path in route:
            return True

        return False
