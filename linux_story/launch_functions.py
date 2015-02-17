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


from linux_story.file_data import copy_data
from linux_story.helper_functions import debugger
from kano_profile.apps import load_app_state_variable


def launch_project(challenge_number="1", step="1"):
    copy_data(int(challenge_number), int(step))
    Step = get_step_class(challenge_number, step)
    Step()


def get_step_class(challenge_number, step_number):
    # Look up fork
    fork = load_app_state_variable(
        'linux-story', 'fork_' + str(challenge_number)
    )

    # If there is a fork, change the module name to add this fork
    if fork:
        module_name = (
            "challenges.challenge_" + challenge_number + '.' + fork + ".steps"
        )
        step_class_name = "Step" + step_number
    else:
        # If no fork, use this module name
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
        print 'Import error = {}, module_name = {}'.format(detail, module_name)
        sys.exit(0)
    else:
        return getattr(module, step_class_name)
