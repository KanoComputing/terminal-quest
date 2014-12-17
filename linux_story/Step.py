#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Step class to describe the flow

import os
from helper_functions import parse_string, typing_animation
from file_functions import write_to_file


class Step():
    story = [""]
    start_dir = "~"
    end_dir = "~"
    command = ""
    hints = ""
    animation = None
    output_condition = lambda x, y: False

    def __init__(self, Terminal_Class):
        self.Terminal = Terminal_Class

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.run()

    def run(self):
        self.save_story()
        # This is to make sure that we clear the terminal properly
        # before printing the story
        write_to_file("started", "")
        self.show_animation()
        self.launch_terminal()
        # Tell storyline the step is finished

        self.next()

    def show_story(self):
        for line in self.story:
            line = parse_string(line, False)
            try:
                typing_animation(line + "\n")
            except:
                pass

    def save_story(self):
        story = "\n".join(self.story)
        write_to_file("story", story)

    def save_hint(self, text):
        write_to_file("hint", text)

    def show_animation(self):
        # if there's animation, play it
        if self.animation:
            try:
                launch_animation(self.animation)
            except:
                # fail silently
                pass

    def next(self):
        pass

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
            self.save_hint("\n" + self.hints[0])
            if len(self.hints) > 1:
                self.hints.pop(0)
        return command_validated and end_dir_validated

    # By default, block cd
    def block_command(self, line):
        line = line.strip()
        if "cd" in line:
            self.save_hint("\nCareful! You don't need cd for this step")
            return True

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
    path = os.path.join(os.path.join(os.path.dirname(__file__), "animation", filename))

    # join command back up
    command = " ".join([path] + elements[1:])

    # run command
    os.system(command)
