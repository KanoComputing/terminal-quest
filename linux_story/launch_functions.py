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

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


import inspect
import challenges
from file_data import copy_data
from helper_functions import print_challenge_title
from challenges import *


def launch_project(challenge_number="1", step="1"):
    os.system("clear")
    print_challenge_title(challenge_number)
    copy_data(challenge_number)
    module = get_challenge_module(challenge_number)
    Step = get_class(module, step)
    Step()


def get_challenge_module(challenge_number):
    module = "challenge_" + challenge_number
    if hasattr(challenges, module):
        return getattr(challenges, module)
    else:
        raise Exception("Cannot find challenge {}".format(challenge_number))


def get_class(module, step):
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and name.find(step) != -1:
            return obj
