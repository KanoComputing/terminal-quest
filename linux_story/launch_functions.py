#!/usr/bin/env python

# launch_functions.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Launch the different processes which show in the terminal

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.load_defaults_into_filetree import default_global_tree


def launch_project(challenge_number=1, step_number=1):

    # TODO: show saved file system if it is available.
    # For now, just show the default filesystem for that step.
    if challenge_number == 0:
        default_global_tree(1, 1)
    else:
        default_global_tree(challenge_number, step_number)

    step = get_step_class(challenge_number, step_number)
    step()


def get_step_class(challenge_number, step_number):

    if challenge_number == 0:
        module_name = "story.challenges.introduction"
        step_class_name = "Step1"
    else:
        # If no fork, use this module name
        module_name = "story.challenges.challenge_{}".format(challenge_number)
        step_class_name = "Step{}".format(step_number)

    try:
        module = __import__(
            module_name,
            globals(),
            locals(),
            [step_class_name],
            -1
        )
    except ImportError as detail:
        print 'Import error = {}, module_name = {}'.format(detail, module_name)
        sys.exit(0)
    else:
        return getattr(module, step_class_name)
