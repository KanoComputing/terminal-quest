# launch_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# The functions which starts off the game at the specified challenge and step.

import sys

from linux_story.common import tq_file_system
from linux_story.file_creation.FileTree import FileTree
from linux_story.load_defaults_into_filetree import default_global_tree
from linux_story.story.trees.default_trees import tree


def launch_project(challenge=1, step=1):
    """
    Start the game off form the specified challenge and step

    Args:
        challenge_number (int)
        step_number (int)

    Returns:
        None
    """
    print "launch_project challenge {}, step {}".format(challenge, step)

    # For now, just show the default filesystem for that step.
    if challenge == 0:
        challenge = 1
        step = 1

    if challenge <= 31:
        default_global_tree(challenge, step)
        step = get_step_class(challenge, step)
        step()
    else:
        from linux_story.ChallengeController import ChallengeController
        from linux_story.MessageClient import MessageClient

        FileTree(tree, tq_file_system).parse_complete(challenge, step)
        client = MessageClient()
        controller = ChallengeController(client)
        controller.run(challenge, step)


def get_step_class(challenge_number, step_number):
    """
    Gets the step class for the specified challenge and step

    Args:
        challenge_number (int)
        step_number (int)

    Returns:
        class which starts the story at the correct point.
    """

    if challenge_number == 0:
        module_name = "story.challenges.introduction"
        step_class_name = "Step1"
    elif challenge_number <= 31:
        # If no fork, use this module name
        module_name = "story.challenges.challenge_{}".format(challenge_number)
        step_class_name = "Step{}".format(step_number)
    else:
        module_name = "story.new_style_challenges.challenge_{}".format(challenge_number)
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
