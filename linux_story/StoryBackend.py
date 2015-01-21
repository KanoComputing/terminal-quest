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
import time

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from helper_functions import (
    parse_string, typing_animation, print_challenge_title
)
from file_functions import (
    append_to_file
    #    file_exists, read_file, delete_file, delete_dir
)
from socket_functions import (
    read_message
)


class StoryBackend():
    def __init__(self):
        self.stop = False
        self.run()

    # Using file functions

    #def run(self):
    #    while not self.stop:
    #        self.next_step()
    #        if file_exists("hint"):
    #            self.read_file("hint")
    #        time.sleep(0.2)

    #def next_step(self):
    #    if file_exists("started"):
    #        delete_file("started")
    #        delete_file("hint")
    #        os.system("clear")
    #        challenge_number = read_file("challenge")
    #        self.print_challenge_title(challenge_number)
    #        self.read_file("story")

    #def read_file(self, message_type):
    #    if file_exists(message_type):
    #        file_contents = read_file(message_type)
    #        delete_file(message_type)
    #        self.type_to_terminal(file_contents, message_type)

    def run(self):
        append_to_file('debug', 'Entered run')

        while not self.stop:
            append_to_file('debug', 'Start of while loop')
            # wait for message
            #message = read_message(['started', 'hint'])
            message = read_message(['hint', 'started'])
            if message.split(' ')[0] == 'started':
                self.next_step()
            else:
                self.type_to_terminal(message, "hint")
                append_to_file("debug", 'hint: {}'.format(message))
                time.sleep(0.2)

    def next_step(self):
        os.system("clear")
        message = read_message(['challenge', 'story'])
        if message.split(' ')[0] == 'challenge':
            print_challenge_title(message)
            story = read_message('story')
            self.type_to_terminal(story, "story")
        else:
            self.type_to_terminal(message, 'story')
            message = read_message('challenge')
            print_challenge_title(message)

    def type_to_terminal(self, text, message_type):
        text = parse_string(text, message_type)
        if message_type == "hint":
            text = "\n" + text
        typing_animation(text)


class StoryThread(threading.Thread):
    def __init__(self, story_ui):
        threading.Thread.__init__(self)
        self.story_ui = story_ui

    # Delete the directory
    #def stop(self):
    #    delete_dir()

    def stop(self):
        pass

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
