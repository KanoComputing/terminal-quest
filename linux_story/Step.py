#!/usr/bin/env python

# Level.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Step class to describe the flow

import os
from helper_functions import parse_string, typing_animation
from terminals.complete_terminal import Complete_Terminal as Terminal


class Step():
    story = [""]
    start_dir = "~"
    end_dir = "~"
    command = ""
    hint = ""
    animation = None

    def __init__(self):
        self.run()

    def run(self):
        self.show_story()
        self.show_animation()
        self.launch_terminal()
        self.next()

    def show_story(self):
        for line in self.story:
            line = parse_string(line, False)
            try:
                typing_animation(line + "\n")
            except:
                pass

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
        Terminal(self.start_dir, self.end_dir, self.command, self.hint)


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
