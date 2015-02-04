#!/usr/bin/env python

# Terminal.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# The template of the terminal classes.

from cmd import Cmd
from helper_functions import (get_completion_desc, get_script_cmd)
from Tree import generate_file_tree

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters. We don't use any functions from this module,
# simply importing this module fixes the bug
import readline


class Terminal(Cmd):
    commands = []

    def __init__(
        self,
        start_dir,
        end_dir,
        check_command,
        block_command,
        check_output
    ):

        Cmd.__init__(self)

        # This changes the special characters, so we can autocomplete on
        # the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))

        self.update_tree()

        self.current_dir = start_dir
        self.current_path = self.filetree[start_dir]
        self.end_dir = end_dir

        # output from last command
        self.last_cmd_output = None

        # validation and check_output should be functions
        self.check_command = check_command
        self.block_command = block_command
        self.check_output = check_output

        self.set_prompt()

        self.cmdloop()

    def set_prompt(self):
        '''Sets prompt according to the current directory
        '''

        self.prompt = self.filetree.generate_prompt(self.current_dir)

    def do_help(self, line):
        '''This is to overwrite the in built function in cmd
        '''

        pass

    def emptyline(self):
        '''To overwrite default behaviour in the cmd module.
        Do nothing if the user enters an empty line.
        '''

        pass

    def update_tree(self):
        '''This updates the model file tree
        Only done after commands that change the file structure
        '''

        self.filetree = generate_file_tree()

    def precmd(self, line):
        '''Hook before the command is run
        If the self.block_command returns True, the command is not run
        Otherwise, it is run
        '''

        if self.block_command(line):
            return Cmd.precmd(self, "")
        else:
            return Cmd.precmd(self, line)

    def onecmd(self, line):

        # Check if value entered is a shell script
        is_script, script = get_script_cmd(
            line,
            self.current_dir,
            self.filetree
        )
        if is_script:
            self.do_shell(script)
        else:
            self.last_cmd_output = Cmd.onecmd(self, line)
            return self.last_cmd_output

    def postcmd(self, stop, line):
        '''If the command output is correct, or if the command typed is
        correct, then return True
        Returning True exits the cmdloop() function
        '''

        cmd_output_correct = self.check_output(self.last_cmd_output)
        return cmd_output_correct or self.check_command(line, self.current_dir)

    def complete_list(self):
        '''Show the list of files in the current directory
        '''

        return list(self.filetree.show_direct_descendents(self.current_dir))

    #######################################################
    # Helper commands

    def autocomplete_desc(self, text, line, completion_type="both"):
        temp_dir = get_completion_desc(self.current_dir, self.filetree,
                                       line, completion_type)
        autocomplete_list = list(self.filetree.show_type(temp_dir,
                                                         completion_type))
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
