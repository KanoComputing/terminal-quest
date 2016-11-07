# terminal_cd.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The a terminal for one of the challenges


import os
import stat
from linux_story.commands_fake import cd
from linux_story.story.terminals.terminal_cat import \
    TerminalCat

# New import
from linux_story.step_helper_functions import route_between_paths


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
        if self.__check_cd():
            self.set_command_blocked(False)
            new_path = cd(self.real_path, line)
            if not not_locked(new_path):
                self.set_command_blocked(True)
                print (
                    _("bash: cd: " + line + ": Permission denied")
                )
            elif new_path:
                self.real_path = new_path
                self.current_path = self.generate_fake_path(self.real_path)
                self.set_prompt()
        else:
            self.set_command_blocked(True)
            print (
                _("Nice try! But you entered an unexpected destination path.")
            )

    def complete_cd(self, text, line, begidx, endidx):
        try:
            return self.autocomplete_files(text, line, begidx, endidx, only_dirs=True)
        except Exception as e:
            print str(e)

    def __check_cd(self):
        """If returns True, that means that cd will bring the user closer
        to their destination, so cd should be allowed to run with the
        user's choice of path.
        """
        if not self.last_user_input.startswith("cd"):
            return False

        # Get the current list of the paths that we're allowed to go on
        route = route_between_paths(self.current_path, self.end_dir)

        if not route:
            route = route_between_paths(self.current_path, self.dirs_to_attempt)

        user_path = self.last_user_input.replace("cd", "").strip()

        if user_path:
            if user_path.startswith("~"):
                new_path = user_path
            else:
                new_path = os.path.join(self.current_path, user_path)
        else:
            # If the user didn't enter a path, assume they want to go to
            # home folder
            new_path = '~'

        new_path = os.path.abspath(os.path.expanduser(new_path))
        if new_path in route:
            return True

        return False
