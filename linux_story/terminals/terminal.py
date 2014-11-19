#!/usr/bin/env python

# Terminal.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The template of the terminal classes.


from cmd import Cmd
from ..helper_functions import (get_completion_desc, parse_string, get_script_cmd,
                                debugger)
from ..Tree import generate_file_tree

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters. We don't use any functions from this module,
# simply importing this module fixes the bug
import readline


class Terminal(Cmd):

    def __init__(self, start_dir, end_dir, validation, hints=[""]):
        Cmd.__init__(self)

        self.update_tree()

        self.current_dir = start_dir
        self.current_path = self.filetree[start_dir]
        self.end_dir = end_dir
        self.validation = validation

        # if hints are a string
        if isinstance(hints, basestring):
            self.hints = [hints]
        # if hints are a array
        else:
            self.hints = hints

        self.set_prompt()
        self.cmdloop()

    def set_prompt(self):
        self.prompt = self.filetree.generate_prompt(self.current_dir)

    def do_help(self, line):
        pass

    def validate(self, line):
        command = True
        end_dir = True

        # if the validation is included
        if self.validation:
            # if only one command can pass the level
            if isinstance(self.validation, basestring):
                command = line == self.validation
            # else there are multiple commands that can pass the level
            else:
                command = line in self.validation
        if self.end_dir:
            end_dir = self.current_dir == self.end_dir

        # if user does not pass challenge, show hints.
        # Go through hints until we get to last hint
        # then just keep showing last hint
        if not (command and end_dir):
            print parse_string(self.hints[0])
            if len(self.hints) > 1:
                self.hints.pop(0)

        return command and end_dir

    # do nothing if the user enters an empty line
    def emptyline(self):
        pass

    # only done after commands that change the file structure
    def update_tree(self):
        self.filetree = generate_file_tree()

    def onecmd(self, value):
        # check if value entered is a shell script
        is_script, script = get_script_cmd(value, self.current_dir, self.filetree)
        if is_script:
            self.do_shell(script)
        else:
            return Cmd.onecmd(self, value)

    # This is the cmd valid command
    def postcmd(self, stop, line):
        return self.validate(line)

    def complete_list(self):
        return list(self.filetree.show_direct_descendents(self.current_dir))

    #######################################################
    # Helper commands

    def autocomplete_desc(self, text, line, completion_type="both"):
        temp_dir = get_completion_desc(self.current_dir, self.filetree,
                                       line, completion_type)
        autocomplete_list = list(self.filetree.show_type(temp_dir, completion_type))
        completions = []
        if not text:
            completions = autocomplete_list[:]
        else:
            for f in autocomplete_list:
                if f.startswith(text):
                    completions.append(f)
            if len(completions) == 1:
                if self.filetree[completions[0]].is_dir:
                    completions[0] += "/"

        return completions

    def autocomplete(self, text, line, complete_list):
        if not text:
            completions = complete_list[:]
        else:
            completions = [f
                           for f in complete_list
                           if f.startswith(text)
                           ]
        return completions
