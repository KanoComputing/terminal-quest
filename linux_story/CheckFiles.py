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
    file_exists, read_file, delete_file, create_dir, FILENAMES
)
from linux_story.gtk3.terminal_ui import Terminal_Ui


class CheckFiles(Terminal_Ui):
    def __init__(self):
        #self.stop = False
        self.run()

    def run(self):
        create_dir()
        while True:
            self.next_step()
            if self.file_exists("hint"):
                self.read_file("hint")

    def file_exists(self, file_name):
        return file_exists(file_name)

    def next_step(self):
        if self.file_exists("started"):
            delete_file("started")
            os.system("clear")
            challenge_number = read_file("challenge")
            self.print_challenge_title(challenge_number)
            self.read_file("story")

    def read_file(self, message_type):
        if self.file_exists(message_type):
            file_contents = read_file(message_type)
            delete_file(message_type)
            self.type_to_terminal(file_contents, message_type)

    def type_to_terminal(self, text, message_type):
        text = parse_string(text, message_type)
        typing_animation(text)

    def print_challenge_title(self, challenge_number="1"):
        print_challenge_title(challenge_number)


class guiThread(threading.Thread):
    def __init__(self, story_ui):
        threading.Thread.__init__(self)
        #self.__stop = False
        self.story_ui = story_ui

    #def stop(self):
    #    for message_type in FILENAMES:
    #        delete_file(message_type)
    #    self.__stop = True

    def run(self):
        path = os.path.abspath(__file__)
        command = "python " + path
        self.story_ui.launch_command(command)


if __name__ == "__main__":
    def sigint_handler(signum, frame):
        pass

    signal.signal(signal.SIGINT, sigint_handler)
    CheckFiles()
