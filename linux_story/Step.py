#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Step class to describe the flow

import os
#from helper_functions import parse_string, typing_animation
#from file_functions import write_to_file
from socket_functions import send_message
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
    challenge_number = 0
    output_condition = lambda x, y: False

    def __init__(self, Terminal_Class):
        self.Terminal = Terminal_Class

        # if hints are a string
        if isinstance(self.hints, basestring):
            self.hints = [self.hints]

        self.run()

    def run(self):
        print 'run'
        self.save_story()

        # This is to make sure that we clear the terminal properly
        # before printing the story
        #write_to_file("started", "")
        send_message("started", "")

        self.show_animation()
        self.launch_terminal()

        if self.last_step:
            self.complete_challenge()

        # Tell storyline the step is finished
        self.next()

    # Unused
    #def show_story(self):
    #    print 'show_story'
    #    for line in self.story:
    #        line = parse_string(line, False)
    #        try:
    #            typing_animation(line + "\n")
    #        except:
    #            pass

    def save_story(self):
        print 'save_story'
        story = "\n".join(self.story)
        #write_to_file("story", story)
        send_message("story", story)

    def save_hint(self, text):
        print 'save_hint'
        #write_to_file("hint", text)
        send_message("hint", text)

    def show_animation(self):
        print 'show_animation'
        # if there's animation, play it
        if self.animation:
            try:
                launch_animation(self.animation)
            except:
                # fail silently
                pass

    def next(self):
        pass

    def complete_challenge(self):
        pass
        #level = load_app_state_variable("linux-story", "level")
        #if self.challenge_number > level:
        #    save_app_state_variable_with_dialog("linux-story", "level",
        #                                        self.challenge_number)

    # default terminal
    def launch_terminal(self):
        print 'launch_terminal'
        self.Terminal(
            self.start_dir,
            self.end_dir,
            self.check_command,
            self.block_command,
            self.check_output
        )

    def check_command(self, line, current_dir):
        print 'check_command'
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
        print 'block_command'
        line = line.strip()
        if "cd" in line:
            return True

    def check_output(self, output):
        print 'check_output'
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
