#!/usr/bin/env python

# run_new_challenges
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import sys
import os

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)
        LOCALE_PATH = os.path.join(dir_path, 'locale')
    else:
        LOCALE_PATH = '/usr/share/locale'

print sys.path


from linux_story.ChallengeController import ChallengeController
from linux_story.MessageClient import MessageClient


def run_new_challenges():
    client = MessageClient()
    controller = ChallengeController(client)

    # Arguments are pipe filename, and then optionally
    # the Challenge and Step numbers
    if len(sys.argv) == 3:
        if sys.argv[1].isdigit() and sys.argv[2].isdigit():
            controller.run(int(sys.argv[1]), int(sys.argv[2]))

    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            controller.run(int(sys.argv[1]), 1)

    elif len(sys.argv) == 1:
        controller.run(1, 1)


if __name__ == "__main__":
    run_new_challenges()