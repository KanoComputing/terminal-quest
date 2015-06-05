#!/usr/bin/env python

# Terminal.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# The template of the terminal classes.

import os
import sys
from cmd import Cmd

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

import threading
from helper_functions import (
    get_script_cmd, debugger, parse_string
)
from socket_functions import is_server_busy, launch_client
from kano.logging import logger
from common import tq_file_system

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters.
import readline


class Terminal(Cmd):
    commands = []

    def __init__(
        self,
        start_path,
        end_path,
        check_command,
        block_command,
        check_output,
        last_cmd_output,
        fake_path,
        finished_challenge,
        get_nano_contents,
        set_nano_running
    ):

        Cmd.__init__(self)

        # This changes the special characters, so we can autocomplete on
        # the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))

        # this should be a complete path
        self.fake_path = fake_path
        self.generate_real_path()
        self.end_dir = end_path

        # output from last command
        self.last_cmd_output = None

        # Validation and check_output should be functions
        # self.check_command = check_command
        self.block_command = block_command
        # self.check_output = check_output
        self.finished_challenge = finished_challenge

        # These are so we can monitor nano in the nano_terminal instance of
        # this class
        self.get_nano_contents = get_nano_contents
        self.set_nano_running = set_nano_running

        self.set_prompt()

    def generate_real_path(self):
        self.real_path = self.fake_path.replace('~', tq_file_system)

    def generate_fake_path(self):
        self.fake_path = self.real_path.replace(tq_file_system, '~')

    def set_prompt(self):
        home_dir = os.path.expanduser('~')
        cwd = self.real_path.replace(home_dir, '~')
        fake_cwd = cwd.replace('/.linux-story', '')

        # if prompt ends with / strip it off
        if fake_cwd[-1] == '/':
            fake_cwd = fake_cwd[:-1]

        # In kano-toolset, but for now want to avoid dependencies
        username = os.environ['LOGNAME']
        prompt = fake_cwd + ' $ '
        # for node in self.show_all_ancestors(fake_cwd):
        #    prompt = node + "/" + prompt
        prompt = "{{Y" + username + "@kano " + "}}" + "{{b" + prompt + "}}"

        coloured_prompt = parse_string(prompt, input=True)
        self.prompt = coloured_prompt

    def do_help(self, line):
        '''This is to overwrite the in built function in cmd
        '''

        pass

    def emptyline(self):
        '''To overwrite default behaviour in the cmd module.
        Do nothing if the user enters an empty line.
        '''

        pass

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

        Check if value entered is a shell script
        '''

        is_script, script = get_script_cmd(
            line,
            self.real_path
        )
        if is_script:
            # TODO: what is this?
            self.do_shell(script)
        else:
            self.last_cmd_output = Cmd.onecmd(self, line)
            return self.last_cmd_output

    def postcmd(self, stop, line):
        '''If the command output is correct, or if the command typed is
        correct, then return True
        Returning True exits the cmdloop() function
        '''

        finished = self.finished_challenge(line)
        return self.finish_if_server_ready(finished)

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

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False):

        try:
            additional_path = line[:int(begidx)].split(" ")[-1]

            # If we do ls ~/ we need to change the path to be absolute.
            if additional_path.startswith('~'):
                # Needs to be moved to helper_functions
                additional_path = additional_path.replace('~', '~/.linux-story')
                # should actually be the hidden-directory
                path = os.path.expanduser(additional_path)
            else:
                path = os.path.join(self.real_path, additional_path)

            # If the path doesn't exist, return early
            if not os.path.exists(path):
                return []

            if text == "..":
                completions = [text]
            elif not text:
                completions = os.listdir(path)
            else:
                contents = os.listdir(path)

                if only_dirs:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text) and
                                   os.path.isdir(os.path.join(path, f))
                                   ]
                else:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text)
                                   ]

            if len(completions) == 1 and \
                    os.path.isdir(os.path.join(path, completions[0])):
                completions = [completions[0] + '/']

            return completions

        except Exception as e:
            logger.debug("hit exception {}".format(str(e)))

    ##################################################################
    # Send info to the server

    def send_text(self, string):
        '''Sends a string through the pipe to the GUI
        '''

        if not is_server_busy():
            data = {'hint': string}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()
