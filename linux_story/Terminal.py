#!/usr/bin/env python

# Terminal.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The template of the terminal classes.


from cmd import Cmd
from helper_functions import (get_completion_desc, get_script_cmd,
                              debugger)
from Tree import generate_file_tree

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters. We don't use any functions from this module,
# simply importing this module fixes the bug
import readline


class Terminal(Cmd):

    def __init__(
        self,
        start_dir,
        end_dir,
        check_command,
        block_command,
        check_output
    ):

        Cmd.__init__(self)

        self.update_tree()

        self.current_dir = start_dir
        self.current_path = self.filetree[start_dir]
        self.end_dir = end_dir

        # validation and check_output should be functions
        self.check_command = check_command
        self.block_command = block_command
        self.check_output = check_output

        self.set_prompt()
        self.cmdloop()

    def set_prompt(self):
        self.prompt = self.filetree.generate_prompt(self.current_dir)

    def do_help(self, line):
        pass

    def validate(self, line):
        return self.validation(line, self.current_dir)

    # do nothing if the user enters an empty line
    def emptyline(self):
        pass

    # only done after commands that change the file structure
    def update_tree(self):
        self.filetree = generate_file_tree()

    def precmd(self, line):
        print "self.block_command(line) = {}".format(self.block_command(line))
        if self.block_command(line):
            return Cmd.precmd(self, "")
        else:
            return Cmd.precmd(self, line)

    def onecmd(self, line):
        # check if value entered is a shell script
        is_script, script = get_script_cmd(line, self.current_dir, self.filetree)
        if is_script:
            self.do_shell(script)
        else:
            print "Cmd.onecmd(self, line) = {}".format(Cmd.onecmd(self, line))
            cmd_output = Cmd.onecmd(self, line)
            print "self.check_output(cmd_output) = {}".format(self.check_output(cmd_output))

    # This is the cmd valid command
    def postcmd(self, stop, line):
        return self.check_command(line, self.current_dir)

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
