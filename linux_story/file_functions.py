#!/usr/bin/env python

# file_functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Functions that read and write to file

import os

DIRECTORY = os.path.join(
    os.path.expanduser("~"),
    "/tmp/linux-story"
)

STORY_FILENAME = os.path.join(
    DIRECTORY,
    "story"
)

HINT_FILENAME = os.path.join(
    DIRECTORY,
    "hint"
)

COMMANDS_FILENAME = os.path.join(
    DIRECTORY,
    "commands"
)

OUTPUT_FILENAME = os.path.join(
    DIRECTORY,
    "output"
)

STARTED_STEP = os.path.join(
    DIRECTORY,
    "started"
)

CHALLENGE_FILENAME = os.path.join(
    DIRECTORY,
    "challenge_number"
)

FILENAMES = {
    "story": STORY_FILENAME,
    "hint": HINT_FILENAME,
    "commands": COMMANDS_FILENAME,
    "output": OUTPUT_FILENAME,
    "started": STARTED_STEP,
    "challenge": CHALLENGE_FILENAME
}

PRINTABLES = {
    "story": STORY_FILENAME,
    "hint": HINT_FILENAME,
    "commands": COMMANDS_FILENAME,
    "output": OUTPUT_FILENAME
}


def create_dir():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)


def write_to_file(file_name, file_contents):
    filename = FILENAMES[file_name]
    f = open(filename, 'w+')
    f.write(file_contents)
    f.close()


def read_file(file_name):
    filename = FILENAMES[file_name]
    with open(filename, "r") as f:
        return f.read()


def file_exists(file_name):
    filename = FILENAMES[file_name]
    if os.path.exists(filename):
        return True
    else:
        return False


def delete_file(file_name):
    filename = FILENAMES[file_name]
    os.remove(filename)
