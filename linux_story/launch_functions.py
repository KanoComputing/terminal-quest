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

from linux_story.Tree import load_global_tree, default_global_tree
from linux_story.common import tq_file_system
from kano_profile.apps import load_app_state_variable


def launch_project(challenge_number=1, step_number=1):

    # TODO: Check the yaml exists in Terminal-Quest-content
    # Warn user otherwise

    # Check save_app_variable_state.  If the program has been loaded before,
    # then the yaml of the file system should exist.
    # If this yaml does not exist, then we should load a warning to the user.

    # TODO: all current users will get a warning, so we need to suppress it
    # for people updating. Maybe update stable-verion to 2?

    # This shows a dialog if the challenge number is inconsistent with the
    # file system e.g. if the file system is missing, or the challenge number
    # is different to the one saved in the profile

    show_dialog = False

    # We don't save the step number.
    level = load_app_state_variable("linux-story", "level")

    if step_number != 1:
        # Only time step_number is not 1 is when someone is testing.
        # Warn tester that the file system will be changed
        show_dialog = True

    if not level:
        # start at challenge 1
        if not challenge_number == 1:
            show_dialog = True

    else:
        if challenge_number != level + 1:
            show_dialog = True
        # if level is defined but the file system has disappeared
        elif not os.path.exists(tq_file_system):
            show_dialog = True

    # We could send a signal to the the GTK side of the app to
    # launch a dialog
    if show_dialog:
        print "showing dialog"

        # TODO: show a dialog telling the user their file system has changed

        # Copy across a default tree
        default_global_tree(challenge_number, step_number)
    else:
        # Initialise the tree from the yaml
        load_global_tree()

    step = get_step_class(challenge_number, step_number)
    step()


def get_step_class(challenge_number, step_number):

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
