#!/usr/bin/env python

# launch_functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Launch the different processes which show in the terminal

import os
import sys
import subprocess

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from linux_story.file_data import copy_data

OPEN_PIPE = None


def open_pipe(pipe_filename):
    global OPEN_PIPE

    # Open pipe
    OPEN_PIPE = open(pipe_filename, 'w')

    # Force it to stay open
    subprocess.Popen(
        ['cat'],
        stdout=OPEN_PIPE,
        stdin=subprocess.PIPE
    )


def get_open_pipe():
    global OPEN_PIPE

    return OPEN_PIPE


def launch_project(pipe_filename, challenge_number="1", step="1"):
    open_pipe(pipe_filename)
    copy_data(int(challenge_number))
    Step = get_step_class(challenge_number, step)
    Step()


def get_step_class(challenge_number, step_number):
    module_name = "challenges.challenge_" + challenge_number + ".steps"
    step_class_name = "Step" + step_number
    try:
        module = __import__(
            module_name,
            globals(),
            locals(),
            [step_class_name],
            -1
        )
    except ImportError as detail:
        print 'Import error = {}'.format(detail)
        return None
    else:
        return getattr(module, step_class_name)
