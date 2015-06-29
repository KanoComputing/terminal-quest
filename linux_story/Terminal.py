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
    get_script_cmd, debugger, parse_string, is_exe
)
from kano_profile.apps import (
    load_app_state_variable, get_app_xp_for_challenge
)
from kano_profile.badges import save_app_state_variable_with_dialog

from socket_functions import is_server_busy, launch_client
from kano.logging import logger
from common import tq_file_system
from load_defaults_into_filetree import delete_item, modify_file_tree
from linux_story.commands_real import run_executable

# If this is not imported, the escape characters used for the colour prompts
# show up as special characters.
import readline


class Terminal(Cmd):
    terminal_commands = []
    print_text = [""]
    story = [""]
    start_dir = "~"
    end_dir = "~"
    commands = ""
    hints = ""
    last_step = False
    challenge_number = ""
    output_condition = lambda x, y: False
    story_dict = {}
    deleted_items = []
    command_blocked = False

    # Trying to merge Step and Terminal
    def __init__(self, xp=""):

        ##################################
        # Initialise the Step stuff first
        self.xp = xp
        self.pipe_busy = False

        # Currently this is passed to the Terminal class but NOT updated
        # because we're making a copy.
        self.last_cmd_output = ""

        # Last command user tried to run.
        self.last_user_input = ""

        # self.current_path is the current path that the user sees
        self.current_path = self.start_dir
        # real_path is the actual filename.
        self.real_path = self.generate_real_path(self.current_path)

        self.modify_file_tree()
        self.delete_items()

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        ##################################

        Cmd.__init__(self)

        # This changes the special characters, so we can autocomplete on
        # the - character
        old_delims = readline.get_completer_delims()
        readline.set_completer_delims(old_delims.replace('-', ''))

        self.set_prompt()
        self.send_start_challenge_data()

        # Need to call .cmdloop() to start terminal class.
        # Maybe put a wrapper function around this if we frequently need to
        # add extra stuff around this.
        self.cmdloop()

        # Once the Terminal has finished, decide whether to add xp to profile
        if self.last_step:
            self.save_challenge()

        # Tell storyline the step is finished
        self.next()

    def generate_real_path(self, fake_path):
        return fake_path.replace('~', tq_file_system)

    def generate_fake_path(self, real_path):
        return real_path.replace(tq_file_system, '~')

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

    def emptyline(self):
        '''To overwrite default behaviour in the cmd module.
        Do nothing if the user enters an empty line.
        '''
        pass

    def do_shell(self, line):
        '''This is run by default if the line starts with !.
        '''
        # We use this over os.system so that the command is run in the
        # correct directory
        run_executable(self.real_path, line)

    def precmd(self, line):
        '''Hook before the command is run
        If the self.block_command returns True, the command is not run
        Otherwise, it is run
        '''

        self.last_user_input = line.strip()

        if self.block_command():
            self.set_command_blocked(True)
            return Cmd.precmd(self, "")
        else:
            self.set_command_blocked(False)
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
            self.do_shell(line)
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
    # Step functions for levelling up

    def next(self):
        '''Defines what should happen next at the end of this step
        Should be modified on inheritance
        '''
        pass

    def block_command(self):
        '''line is the user entered input from the terminal.
        If this function returns True, input entered will be blocked
        Otherwise, command will be run as normal.
        Default behaviour is to block cd and mv
        '''

        if "cd" in self.last_user_input or \
                "mkdir" in self.last_user_input or \
                ("mv" in self.last_user_input and
                    not self.last_user_input == 'mv --help'):

            print ('Nice try! But you do not need that command for this '
                   'challenge')

            return True

    def check_output(self, output):
        '''Use output of the command to level up.
        The argument is the output from the command printed in the terminal.
        If the function return True, will break out of cmdloop and go to next
        Step.
        if the function returns False, whether the level passes depends on
        the return value of self.check_command
        '''
        if not output:
            return False

        output = output.strip()
        return self.output_condition(output)

    def finished_challenge(self, line):
        '''If this returns True, we exit the cmdloop.
        If this return False, we stay in the cmdloop.

        Depending on the challenge, we may want to either pass only
        depending on the output, but not on the command.  So we may want
        to change this in an instance of the Step class.
        '''
        finished = self.check_output(self.last_cmd_output) or \
            self.check_command()

        return finished

    def check_command(self):
        '''If self.commands is provided, checks the command entered
        by the user matches self.commands.
        '''

        # check through list of commands
        command_validated = True
        end_dir_validated = True

        # if the validation is included
        if self.commands:
            # if only one command can pass the level
            if isinstance(self.commands, basestring):
                command_validated = (self.last_user_input == self.commands)
            # else there are multiple commands that can pass the level
            else:
                command_validated = self.last_user_input in self.commands

        if self.end_dir:
            end_dir_validated = self.current_path == self.end_dir

        if not (command_validated and end_dir_validated):
            self.show_hint()

        condition = (command_validated and end_dir_validated)
        return self.finish_if_server_ready(condition)

    #######################################################
    # Send text to the GUI.

    def show_hint(self):
        '''Customize the hint that is shown to the user
        depending on their input.
        Default behaviour, display normal hint.
        '''
        # Default behaviour
        # if user does not pass challenge, show hints.
        # Go through hints until we get to last hint
        # then just keep showing last hint

        # The last line the user typed is self.last_user_input

        self.send_hint()

    def send_hint(self, hint=None):
        '''Sends a hint string through the pipe to the GUI
        '''

        if not is_server_busy():
            if not hint:
                hint = '\n' + self.hints[0]
            else:
                hint = '\n' + hint
            data = {'hint': hint}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()

        if len(self.hints) > 1:
            self.hints.pop(0)

    def send_text(self, string):
        '''Sends a string through the pipe to the GUI
        '''
        if not is_server_busy():
            data = {'hint': string}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()

    def send_start_challenge_data(self):
        '''Sends all the relevent information at the start of a new step
        '''

        data = {}

        # Get data about any XP.
        data['xp'] = self.xp
        data["print_text"] = "\n".join(self.print_text)
        data['story'] = "\n".join(self.story)
        data['challenge'] = str(self.challenge_number)
        data['spells'] = self.terminal_commands

        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def get_xp(self):
        '''Look up XP earned after challenge
        '''
        # Look up XP earned
        xp = get_app_xp_for_challenge("linux-story",
                                      str(self.challenge_number)
                                      )

        if xp > 0:
            self.xp = "{{gb:Congratulations, you earned " + str(xp) + " XP!}}\n\n"

    def exit(self):
        data = {'exit': '1'}
        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    ######################################################
    # Kano world integration

    def save_challenge(self):
        '''Integration with kano world
        '''
        level = load_app_state_variable("linux-story", "level")

        if self.challenge_number > level:
            save_app_state_variable_with_dialog("linux-story", "level",
                                                self.challenge_number)
            self.get_xp()

    #######################################################
    # File system functions

    def delete_items(self):
        '''self.deleted_items should be a list of fake_paths we want removed
        '''
        if self.deleted_items:
            for path in self.deleted_items:

                # TODO: move this to common
                real_path = os.path.expanduser(
                    path.replace('~', '~/.linux-story')
                )
                delete_item(real_path)

    def modify_file_tree(self):
        '''If self.story_dict is specified, add files to the filetree
        '''
        if self.story_dict:
            modify_file_tree(self.story_dict)

    #######################################################
    # Helper commands

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False,
                           only_exe=False):

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
            # TODO: move this part to a separate function?
            # Then we can have a list of all the functions that get called
            if not os.path.exists(path):
                return []

            if text == "..":
                completions = [text]
            elif not text and line == "./":
                # This is repeated
                contents = os.listdir(path)
                completions = [f
                               for f in contents
                               if f.startswith(text) and (
                                   os.path.isdir(os.path.join(path, f)) or
                                   is_exe(os.path.join(path, f)))
                               ]
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
                elif only_exe:
                    completions = [f
                                   for f in contents
                                   if f.startswith(text) and (
                                       os.path.isdir(os.path.join(path, f)) or
                                       is_exe(os.path.join(path, f)))
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

    # Overwrite this to check for shell scripts instead.
    def completedefault(self, *ignored):
        '''ignored = [text, line, begidx, endidx]
        text = (string I think?) ?
        line = (string) line the user entered
        begidx = (int) ?
        endidx = (int) ?
        '''
        [text, line, begidx, endidx] = ignored
        return self.autocomplete_files(
            text, line, begidx, endidx, only_exe=True
        )

    def complete_executable(self, text, line, begidx, endidx):
        # Asssuming the input is of the form.
        return ["./"]

    # The original text from the cmd module.
    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """

        if state == 0:
            import readline
            origline = readline.get_line_buffer()
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = readline.get_begidx() - stripped
            endidx = readline.get_endidx() - stripped
            if begidx > 0:
                cmd, args, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            else:
                # Modified this so we check for executables sometimes
                if line == ".":
                    compfunc = self.complete_executable
                else:
                    compfunc = self.completenames
            self.completion_matches = compfunc(text, line, begidx, endidx)
        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    #######################################################
    # Set whether command has been blocked

    def set_command_blocked(self, blocked):
        self.command_blocked = blocked

    def get_command_blocked(self):
        return self.command_blocked
