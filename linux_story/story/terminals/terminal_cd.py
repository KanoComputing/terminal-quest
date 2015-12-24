#!/usr/bin/env python

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The a terminal for one of the challenges

import os

from linux_story.story.terminals.terminal_cat import (
    TerminalCat
)

from linux_story.commands_fake import cd

# New import
from linux_story.step_helper_functions import route_between_paths


class TerminalCd(TerminalCat):
    terminal_commands = ["ls", "cat", "cd"]

    def do_cd(self, line, has_access=True):
        if self.check_cd():
            self.set_command_blocked(False)
            new_path = cd(self.real_path, line)

            if new_path:
                self.real_path = new_path
                self.current_path = self.generate_fake_path(self.real_path)
                self.set_prompt()
        else:
            self.set_command_blocked(True)
            print (
                "Nice try! But you entered an unexpected destination path."
            )

    def complete_cd(self, text, line, begidx, endidx):
        try:
            return self.autocomplete_files(text, line, begidx, endidx, only_dirs=True)
        except Exception as e:
            print str(e)

    def check_cd(self):
        '''If returns True, that means that cd will bring the user closer
        to their destination, so cd should be allowed to run with the
        user's choice of path.
        '''

        # Get the current list of the paths that we're allowed to go on
        route = route_between_paths(self.current_path, self.end_dir)

        if not self.last_user_input.startswith("cd"):
            return False

        # Check the path the user entered
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
