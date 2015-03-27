#!/usr/bin/env python

# get_defaults.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Get the default file system for when the user corrupts the saved version on
# their system


import os
import yaml
import sys


if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


# All the files needed for the system are in a directory, each with a unique
# name.  The defaults are stored in a yaml like below

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


# We take only the relevent challenge, which can
# then be processed by the StoryFileTree class


def get_default_file_dict(challenge_number, step_number):
    '''This takes the default settings from the yaml containing defaults,
    and changes into a dictionary which is suitable for the Tree class
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
    '''Get the filepath to the default tree yaml
    '''

    current_dir = os.path.abspath(os.path.dirname(__file__))
    default_tree_config = os.path.join(current_dir,
                                       "story/trees/default_trees.yml")
    return default_tree_config


def filter_later_challenges(data_dict, current_challenge, current_step):
    '''This is the first filter though the default yaml

    Go through the yaml, and take out the challenges that are greater
    than the ones we're interested in.

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

    i.e. an id might appear multiple times across different dicitonaries

    Return a dictionary with the names separated and cuts out all the
    challenges and steps which are greater than the ones we're interested in
    '''

    # TODO: be consistent with whether the chalenge and step numbers
    # are strings or integers
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

        # Here we change the structure of the dictionary, so instead of a
        filenames = dict_id.split(', ')
        for name in filenames:

            # if challenges in the data dictionary, remove all challenges
            # greater than the one we're considering now

            if name in draft_story_dict.keys():
                # Analyse tree[name] and try and blend the
                # two together print challenge_dict['challenges']

                if 'challenges' in draft_story_dict[name]:
                    draft_story_dict[name]['challenges'] += data_dict['challenges']
                else:
                    draft_story_dict[name]['challenges'] = data_dict['challenges']

            else:
                draft_story_dict[name] = data_dict

    return draft_story_dict


def get_relevant_challenge(draft_story_dict):
    '''Order the array of dictiories by the challenge, and then step.
    We can then take the last element of the ordered dictionaries, and this
    will be the relevent challenge.
    '''

    story_dict = {}
    for name, file_dict in draft_story_dict.iteritems():

        if 'challenges' in file_dict:
            challenge_array = file_dict['challenges']

            sorted_challenges = sorted(
                challenge_array, key=lambda k: (k['challenge'], k['step'])
            )

            # If the list is non empty,
            # only last element should be relevent
            if sorted_challenges:
                story_dict[name] = {}
                story_dict[name] = sorted_challenges[-1]

                if 'name' in file_dict:
                    story_dict[name]['name'] = file_dict['name']

    return story_dict
