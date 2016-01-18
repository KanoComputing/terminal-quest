# get_defaults.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Get filesystem information for the specified challenge/step

# All the files needed for the system are in a directory, each with a unique
# name. The defaults are stored in a yaml like below.

# Mum:
#    challenges:
#        - challenge: 1
#          step: 1
#          path: "~/my-house/kitchen"

#        - challenge: 8
#          step: 1
#          exists: False

# note_greenhouse:
#   name: "note"
#   challenges:
#       - challenge: 1
#         challenge: 3
#         path: "~/my-house/garden/greenhouse"

# We take only the relevent challenge, which can then be
# processed by the StoryFileTree class.


import os
import sys
import yaml
from copy import deepcopy

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


def get_default_file_dict(challenge_number, step_number):
    '''
    This takes the yaml containing information about the defaults,
    and changes into a dictionary which is suitable for the Tree class.

    Args:
        challenge_number (str): The challenge number we want to find file
            information about.
        step_number (str): The step number we want to find the file information
            about.

    Returns:
        dict: containing only information about the specified challenge and
            step.
    '''

    default_tree_config = get_default_tree_filename()
    stream = open(default_tree_config)
    data_dict = yaml.load(stream)

    draft_story_dict = filter_later_challenges(
        data_dict, challenge_number, step_number
    )

    story_dict = get_relevant_challenge(draft_story_dict)
    return story_dict


def get_default_tree_filename():
    '''
    Returns:
        str: filepath to yaml containing the default tree information.
    '''

    current_dir = os.path.abspath(os.path.dirname(__file__))
    default_tree_config = os.path.join(current_dir,
                                       "story/trees/default_trees.yaml")
    return default_tree_config


def filter_later_challenges(data_dict, current_challenge, current_step):
    '''
    This is the first filter though the default yaml. It removes the
    information about all later challenges/steps.

    Input dictionary is of the form:
    {
        'robot, flower, window': {
            'challenges': [
                {
                    'challenge': 1,
                    'step': 1,
                    'path': '~/my-house/my-room'
                }
            ]
        },

        'robot': {
            'challenges': [
                {
                    'challenge': 2,
                    'step': 3
                    'path': '~/my-house
                }
            ]
        }
    }

    i.e. a file id might appear multiple times across different ids.

    Args:
        current_challenge (str)
        current_step (str)
        data_dict (dict): This is all the information about the file system
            across all the different challenges.
            e.g. the story/trees/default_trees.yaml is an example dictionary.

    Returns:
        dict: Return a dictionary with the names separated
            (instead of being muddled up together) and cuts out all the
            challenges and steps which are greater than the one specified.
    '''

    current_challenge = int(current_challenge)
    current_step = int(current_step)

    draft_story_dict = {}

    # Go through the config file
    for dict_id, data_dict in data_dict.iteritems():

        # Filter relevent challenges in data_dict
        if 'challenges' in data_dict.keys():

            # If the challenges go above the challenge we're
            # considering, we can immediately block it and
            # return the last element
            stored_challenges = data_dict['challenges']
            relevant_challenges = []

            for challenge in stored_challenges:

                # Only accept challenges that are <= to the current
                # challenge.
                # Anything above is irrelevant.
                if challenge['challenge'] < current_challenge or \
                   (challenge['challenge'] == current_challenge and
                        challenge['step'] <= current_step):

                    # Only if these point apply do you add it to the
                    # tree.
                    relevant_challenges.append(challenge)

            data_dict['challenges'] = relevant_challenges

            # We don't have all the information yet, so we can't
            # reorder the elements yet

        # Here we change the structure of the dictionary
        filenames = dict_id.split(', ')
        for name in filenames:
            # If challenges in the data dictionary, remove all challenges
            # greater than the one we're considering now.

            if name in draft_story_dict.keys():
                # Analyse tree[name] and try and blend the
                # two together.

                if 'challenges' in draft_story_dict[name]:
                    draft_story_dict[name]['challenges'] += data_dict['challenges']
                else:
                    draft_story_dict[name]['challenges'] = data_dict['challenges']

            else:
                draft_story_dict[name] = deepcopy(data_dict)

    return draft_story_dict


def get_relevant_challenge(draft_story_dict):
    '''
    Order the array of dictiories by the challenge, and then step.
    We can then take the last element of the ordered dictionaries, and this
    will be the relevent challenge.

    Args:
        draft_story_dict (dict): output from filter_later_challenges.
            Dictionary of the all ids (representing the unique files in
            the story_files folder) with information about later challenges
            cut out.

    Returns:
        dict: Of the same form but only with information about the specified
            challenges.
    '''

    story_dict = {}
    for name, file_dict in draft_story_dict.iteritems():

        # Check if 'challenges' is in the file_dict - if not, then this
        # file shouldn't be added to the dictionary
        if 'challenges' in file_dict:

            # initialise story_dict
            story_dict[name] = {}

            # Go through the keys in the dictionary.  If the key is
            # 'challenges, filter the challenges.  Otherwise, just
            # copy them across
            for key in file_dict.keys():
                if key == 'challenges':
                    challenge_array = file_dict['challenges']

                    sorted_challenges = sorted(
                        challenge_array, key=lambda k: (k['challenge'], k['step'])
                    )

                    # If the list is non empty,
                    # only last element should be relevent
                    if sorted_challenges:
                        story_dict[name].update(sorted_challenges[-1])

                        if 'name' in file_dict:
                            story_dict[name]['name'] = file_dict['name']

                else:
                    story_dict[name][key] = file_dict[key]

            # If at the end, story_dict[name]["challenge"] is empty,
            # then delete the entry since that file shouldn't exist for
            # the specified challenge/step combo
            if 'challenge' not in story_dict[name]:
                del story_dict[name]

    return story_dict
