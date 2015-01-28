#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Step class to describe the flow

import os
import json
from launch_functions import get_open_pipe
#from kano_profile.badges import save_app_state_variable_with_dialog
#from kano_profile.apps import load_app_state_variable


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

        # Available commands that can be used in the Terminal
        self.commands = self.Terminal.commands

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.run()

    def write_to_pipe(self, information):
        f = get_open_pipe()
        print >> f, information
        f.flush()

    def run(self):
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

    def send_hint(self):
        hint = '\n' + self.hints[0]
        data = json.dumps({'hint': hint})
        self.write_to_pipe(data)

    def send_start_challenge_data(self):
        data = {}
        data['story'] = "\n".join(self.story)
        data['challenge'] = str(self.challenge_number)
        data['spells'] = self.commands
        str_data = json.dumps(data)
        self.write_to_pipe(str_data)

    def show_animation(self):
        # if there's animation, play it
        if self.animation:
            try:
                launch_animation(self.animation)
            except:
                # fail silently
                pass

    # Changed on inheritance
    def next(self):
        pass

    # Integration with Kano World
    def complete_challenge(self):
        pass
        #level = load_app_state_variable("linux-story", "level")
        #if self.challenge_number > level:
        #    save_app_state_variable_with_dialog("linux-story", "level",
        #                                        self.challenge_number)

    # default terminal
    def launch_terminal(self):
        self.Terminal(
            self.start_dir,
            self.end_dir,
            self.check_command,
            self.block_command,
            self.check_output
        )

    def check_command(self, line, current_dir):
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

        # if user does not pass challenge, show hints.
        # Go through hints until we get to last hint
        # then just keep showing last hint
        if not (command_validated and end_dir_validated):
            #self.save_hint("\n" + self.hints[0])
            self.send_hint()

            if len(self.hints) > 1:
                self.hints.pop(0)

        return command_validated and end_dir_validated

    # By default, block cd
    def block_command(self, line):
        line = line.strip()
        if "cd" in line:
            return True

    # Use output of command to level up
    def check_output(self, output):
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
