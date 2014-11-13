#!/usr/bin/env python

# launch_functions.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# Launch the different processes which show in the terminal


import inspect
import challenges
from challenges import *


def launch_project(challenge_number="1", step="1"):
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
