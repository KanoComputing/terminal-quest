"""
* Copyright (C) 2014 Kano Computing Ltd
* License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
*
* Author: Caroline Clark <caroline@kano.me>
* Launch the different processes which show in the terminal
"""

import os
import json

from linux_story.Terminals import Terminal
from linux_story.helper_functions import (copy_file_tree, parse_string)


def launch_project(chapter_number=1, terminal_number=1):

    chapters = []
    filepath = get_chapter_path(chapter_number)

    while os.path.exists(filepath):
        file_contents = ""
        with open(filepath) as infile:
            file_contents = infile.read().strip()
        challenges = json.loads(file_contents)
        chapters.append(challenges)
        chapter_number = chapter_number + 1
        filepath = get_chapter_path(chapter_number)

    for chapter in chapters:
        # find total number of challenges
        keys = [int(x) for x in chapter.keys()]
        last_challenge = int(sorted(keys)[-1])

        for i in range(terminal_number, last_challenge + 1):
            launch_challenge_number(i, chapter)


def get_chapter_path(chapter_number):
    filepath = os.path.join(os.path.dirname(__file__), "data/chapter_" + str(chapter_number) + ".json")
    return filepath


def launch_challenge_number(terminal_number, challenges):
    challenge_dict = challenges[str(terminal_number)]
    for line in challenge_dict["story"]:
        line = parse_string(line, True)
        try:
            raw_input(line)
        except:
            pass

    # if there's animation, play it
    try:
        animation_cmd = challenge_dict["animation"]
        launch_animation(animation_cmd)
    except:
        # fail silently
        pass

    start_dir = challenge_dict["start_dir"]
    end_dir = challenge_dict["end_dir"]
    command = challenge_dict["command"]
    hint = challenge_dict["hint"]
    copy_file_tree(terminal_number)
    Terminal(start_dir, end_dir, command, hint)


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
