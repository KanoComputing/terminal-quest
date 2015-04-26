#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Step class to describe the flow

import threading
import os
from socket_functions import launch_client, is_server_busy
from kano_profile.badges import save_app_state_variable_with_dialog
from kano_profile.apps import (
    load_app_state_variable, get_app_xp_for_challenge
)
from load_defaults_into_filetree import delete_item, modify_file_tree


class Step():
    story = [""]
    start_dir = "~"
    end_dir = "~"
    commands = ""
    hints = ""
    last_step = False
    challenge_number = 1
    step_number = 1
    output_condition = lambda x, y: False
    story_dict = {}
    deleted_items = []
    xp = ""

    # We can either tree as a global variable in common, or pass it as a
    # variable between the files.
    # We have to be careful with tree, as it has to be accessed from the right
    # thread otherwise the old data is erased.
    def __init__(self, Terminal_Class, xp=""):

        self.xp = xp
        self.pipe_busy = False

        self.modify_file_tree()
        self.delete_items()

        # Available commands that can be used in the Terminal
        self.terminal_commands = Terminal_Class.commands

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.terminal = Terminal_Class(
            self.start_dir,
            self.end_dir,
            self.check_command,
            self.block_command,
            self.check_output
        )

        self.run()

    def run(self):
        '''Runs through the Step, which does the following:
        - Displays the challenge number at the top
        - Types out the story
        - Creates the new personalised Terminal with the available commands
        - Once the terminal exits, takes you to the next Step
        '''

        # Save the challenge information on run.
        # We would save on every step, but it's a little too
        # slow to do this since save_app_state_variable refreshes kdesk

        # Send all story data together
        self.send_start_challenge_data()
        self.launch_terminal()

        if self.last_step:
            self.save_challenge()

        # Tell storyline the step is finished
        self.next()

    def exit(self):
        data = {'exit': '1'}
        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def send_text(self, string):
        '''Sends a string through the pipe to the GUI
        '''

        if not is_server_busy():
            data = {'hint': string}
            t = threading.Thread(target=launch_client, args=(data,))
            t.daemon = True
            t.start()

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

    def send_start_challenge_data(self):
        '''Sends all the relevent information at the start of a new step
        '''

        data = {}

        # Get data about any XP.
        data['xp'] = self.xp

        data['story'] = "\n".join(self.story)
        data['challenge'] = str(self.challenge_number)
        data['spells'] = self.terminal_commands
        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def next(self):
        '''Defines what should happen next at the end of this step
        Should be modified on inheritance
        '''

        pass

    def delete_items(self):
        '''self.delete_items should be a list of fake_paths we want removed
        '''
        if self.deleted_items:
            for path in self.deleted_items:

                # TODO: move this to common
                real_path = os.path.expanduser(path.replace('~', '~/.linux-story'))
                delete_item(real_path)

    def get_xp(self):
        '''Look up XP earned after challenge
        '''
        # Look up XP earned
        xp = get_app_xp_for_challenge("linux-story",
                                      str(self.challenge_number)
                                      )

        if xp > 0:
            self.xp = "{{gb:Congratulations, you earned " + str(xp) + " XP!}}\n\n"

    def save_challenge(self):
        '''Integration with kano world
        '''

        level = load_app_state_variable("linux-story", "level")
        if self.challenge_number > level:
            save_app_state_variable_with_dialog("linux-story", "level",
                                                self.challenge_number)
            self.get_xp()

    def launch_terminal(self):
        '''Starts off the terminal's game loop.
        This function does not stop until the user has passed the level
        '''

        self.terminal.cmdloop()

    def check_command(self, line, current_dir):
        '''If self.commands is provided, checks the command entered
        by the user matches self.commands.
        '''

        print "line = {}".format(line)
        print "current_dir = {}".format(current_dir)

        # check through list of commands
        command_validated = True
        end_dir_validated = True

        # strip any spaces off the beginning and end
        line = line.strip()

        # if the validation is included
        if self.commands:
            # if only one command can pass the level
            if isinstance(self.commands, basestring):
                command_validated = line == self.commands
            # else there are multiple commands that can pass the level
            else:
                command_validated = line in self.commands

        if self.end_dir:
            end_dir_validated = current_dir == self.end_dir

        if not (command_validated and end_dir_validated):
            self.show_hint(line, current_dir)

        condition = (command_validated and end_dir_validated)
        return self.finish_if_server_ready(condition)

    def finish_if_server_ready(self, other_condition):
        print "in if_server_ready"
        return self.terminal.finish_if_server_ready(other_condition)

    def show_hint(self, line, current_dir):
        '''Customize the hint that is shown to the user
        depending on their input
        '''
        # Default behaviour
        # if user does not pass challenge, show hints.
        # Go through hints until we get to last hint
        # then just keep showing last hint
        self.send_hint()

        if len(self.hints) > 1:
            self.hints.pop(0)

    def block_command(self, line):
        '''line is the user entered input from the terminal.
        If this function returns True, input entered will be blocked
        Otherwise, command will be run as normal.
        Default behaviour is to block cd and mv
        '''

        line = line.strip()
        if "cd" in line or "mkdir" in line or \
                ("mv" in line and not line == 'mv --help'):

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

    def modify_file_tree(self):
        '''If self.story_dict is specified, add files to the filetree
        '''
        if self.story_dict:
            modify_file_tree(self.story_dict)
