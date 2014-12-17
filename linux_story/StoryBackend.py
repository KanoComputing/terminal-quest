#!/usr/bin/env python

# Step.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Class which shows the contents of hints and storyline files in tmp

import os
import sys
import threading
import signal

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from helper_functions import (
    parse_string, typing_animation, print_challenge_title
)
from file_functions import (
    file_exists, read_file, delete_file, delete_dir
)


class StoryBackend():
    def __init__(self):
        self.stop = False
        self.run()

    def run(self):
        while not self.stop:
            self.next_step()
            if file_exists("hint"):
                self.read_file("hint")

    def next_step(self):
        if file_exists("started"):
            delete_file("started")
            delete_file("hint")
            os.system("clear")
            challenge_number = read_file("challenge")
            self.print_challenge_title(challenge_number)
            self.read_file("story")

    def read_file(self, message_type):
        if file_exists(message_type):
            file_contents = read_file(message_type)
            delete_file(message_type)
            self.type_to_terminal(file_contents, message_type)

    def type_to_terminal(self, text, message_type):
        text = parse_string(text, message_type)
        if message_type == "hint":
            text = "\n" + text
        typing_animation(text)

    def print_challenge_title(self, challenge_number="1"):
        print_challenge_title(challenge_number)


class StoryThread(threading.Thread):
    def __init__(self, story_ui):
        threading.Thread.__init__(self)
        self.story_ui = story_ui

    def stop(self):
        delete_dir()

    def run(self):
        path = os.path.abspath(__file__)
        command = "python " + path
        self.story_ui.launch_command(command)
        self.stop()


if __name__ == "__main__":
    def sigint_handler(signum, frame):
        pass

    signal.signal(signal.SIGINT, sigint_handler)
    StoryBackend()
