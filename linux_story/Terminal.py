#!/usr/bin/env python

# Terminal.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The template of the terminal classes.

from cmd import Cmd
from helper_functions import (
    get_completion_desc, get_script_cmd, debugger
)
from Tree import generate_file_tree
from socket_functions import is_server_busy

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters.
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
        '''Modified Cmd.cmd.onecmd so that it can detect if a file is a script,
        and can run it appropriately

        Keyword arguments:
        line - string.  Is what the user enters at the terminal
        '''

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
        condition = cmd_output_correct or self.check_command(line, self.current_dir)
        return self.finish_if_server_ready(condition)

    def complete_list(self):
        '''Show the list of files in the current directory
        '''

        return list(self.filetree.show_direct_descendents(self.current_dir))

    @staticmethod
    def finish_if_server_ready(other_condition):
        server_busy = is_server_busy()
        debugger("server_busy = {}".format(server_busy))
        debugger('other_condition = {}'.format(other_condition))
        will_finish = (not server_busy and other_condition)
        debugger('will finish = {}'.format(will_finish))
        return will_finish

    #######################################################
    # Helper commands

    def autocomplete_desc(self, text, line, completion_type="both"):
        '''This is used to autcomplete the next file/folder

        Keyword arguments:
        text, string, is the last part you are trying to autocomplete
        line, string, is the line so far entered by the user in the terminal
        completion_type, string. Can be 'file', 'dir' or 'both'
        '''

        try:
            temp_dir = get_completion_desc(
                self.current_dir, self.filetree, line, completion_type
            )

            autocomplete_list = list(
                self.filetree.show_files_or_dirs(
                    temp_dir,
                    completion_type
                )
            )

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

        except Exception as e:
            return ["Exception caught = {}".format(e)]

    def autocomplete(self, text, line, complete_list):
        if not text:
            completions = complete_list[:]
        else:
            completions = [f
                           for f in complete_list
                           if f.startswith(text)
                           ]
        return completions
