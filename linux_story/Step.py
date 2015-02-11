#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Step class to describe the flow

import os
import threading
from socket_functions import launch_client, is_server_busy
# from kano_profile.badges import save_app_state_variable_with_dialog
# from kano_profile.apps import load_app_state_variable


class Step():
    story = [""]
    start_dir = "~"
    end_dir = "~"
    command = ""
    hints = ""
    animation = None
    last_step = False
    challenge_number = 1
    output_condition = lambda x, y: False

    def __init__(self, Terminal_Class):
        self.Terminal = Terminal_Class
        self.pipe_busy = False

        # Available commands that can be used in the Terminal
        self.commands = self.Terminal.commands

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.run()

    def run(self):
        '''Runs through the Step, which does the following:
        - Displays the challenge number at the top
        - Types out the story
        - Creates the new personalised Terminal with the available commands
        - Once the terminal exits, takes you to the next Step
        '''

        # Send all story data together
        self.send_start_challenge_data()

        # TODO: Disable terminal while story is running?

        # Show animation if present here
        self.show_animation()
        self.launch_terminal()

        # Structure copied from snake
        if self.last_step:
            self.complete_challenge()

        # Tell storyline the step is finished
        self.next()

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
        data['story'] = "\n".join(self.story)
        data['challenge'] = str(self.challenge_number)
        data['spells'] = self.commands
        t = threading.Thread(target=launch_client, args=(data,))
        t.daemon = True
        t.start()

    def show_animation(self):
        # if there's animation, play it
        if self.animation:
            try:
                launch_animation(self.animation)
            except:
                # fail silently
                pass

    def next(self):
        '''Defines what should happen next at the end of this step
        Should be modified on inheritance
        '''

        pass

    def complete_challenge(self):
        '''Integration with kano world
        '''

        pass
        #level = load_app_state_variable("linux-story", "level")
        #if self.challenge_number > level:
        #    save_app_state_variable_with_dialog("linux-story", "level",
        #                                        self.challenge_number)

    def launch_terminal(self):
        '''Launches the terminal.
        self.cmdloop is start in the __init__ of the Terminal class
        '''

        self.Terminal(
            self.start_dir,
            self.end_dir,
            self.check_command,
            self.block_command,
            self.check_output
        )

    def check_command(self, line, current_dir):
        '''If self.command is provided, checks the command entered
        by the user matches self.command.
        '''

        # check through list of commands
        command_validated = True
        end_dir_validated = True

        # strip any spaces off the beginning and end
        line = line.strip()

        # if the validation is included
        if self.command:
            # if only one command can pass the level
            if isinstance(self.command, basestring):
                command_validated = line == self.command
            # else there are multiple commands that can pass the level
            else:
                command_validated = line in self.command

        if self.end_dir:
            end_dir_validated = current_dir == self.end_dir

        if not (command_validated and end_dir_validated):
            self.show_hint(line, current_dir)

        condition = (command_validated and end_dir_validated)
        return self.finish_if_server_ready(condition)

    def finish_if_server_ready(self, other_condition):
        return self.Terminal.finish_if_server_ready(other_condition)

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
        if "cd" in line or "mv" in line:
            return True

    def check_output(self, output):
        '''Use output of the command to level up.
        The argument is the output from the command printed in the terminal.
        If the function return True, will break out of cmdloop and go to next
        Step.
        if the function returns False, will stay in this Step.
        '''

        if not output:
            return False

        output = output.strip()
        return self.output_condition(output)


def launch_animation(command):
    # split the command into it's components
    elements = command.split(" ")

    # the filename is the first element
    filename = elements[0]

    # find complete path
    path = os.path.join(
        os.path.join(
            os.path.dirname(__file__),
            "animation", filename
        )
    )

    # join command back up
    command = " ".join([path] + elements[1:])

    # run command
    os.system(command)
