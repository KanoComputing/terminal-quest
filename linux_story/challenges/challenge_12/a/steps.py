#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.challenges.challenge_11.terminals import TerminalMv
from linux_story.file_data import HIDDEN_DIR, copy_data
from linux_story.challenges.challenge_13.a.steps import Step1 as LoseGirl
from linux_story.challenges.challenge_13.b.steps import Step1 as SaveGirl
from linux_story.helper_functions import play_sound


class StepTemplateMv(Step):
    challenge_number = 12

    def __init__(self):
        Step.__init__(self, TerminalMv)


# You lose the dog
class Step1(StepTemplateMv):
    story = [
        "{{wb:Edith:}} {{wn:Oh no!  I heard the sound of a bell.",
        "Check that my little girl is alright!}}"
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"

    command = [
        "ls ..",
        "ls ../",
        "ls -a ..",
        "ls -a ../",
        "ls ~/town",
        "ls ~/town/",
        "ls -a ~/town",
        "ls -a ~/town/"
    ]

    hints = [
        "{{rn:Use the command}} {{yb:ls ..}} {{rn:to look in the lower "
        "directory}}"
    ]

    def __init__(self):
        self.save_fork('a')
        StepTemplateMv.__init__(self)

    def next(self):
        Step2()


# Put dramatic music here?  Or loop some track
class Step2(StepTemplateMv):
    story = [
        "{{wn:The dog has disappeared!}}\n",
        # Ideally, make this font slightly smaller
        "{{wb:Eleanor:}} {{wn:Oh no!  Doggy gone!",
        "....am I next?}}\n",

        # Normal sized
        "{{wb:Edith:}} {{wn:Get my daughter back!}}"
    ]

    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "mv ../Eleanor .",
        "mv ../Eleanor ./",
        "mv ~/town/Eleanor ~/town/.hidden-shelter",
        "mv ~/town/Eleanor ~/town/.hidden-shelter/",
        "mv ~/town/Eleanor .",
        "mv ~/town/Eleanor ./",
        "mv ../Eleanor ~/town/.hidden-shelter",
        "mv ../Eleanor ~/town/.hidden-shelter/",
    ]
    hints = [
        "{{r:Use the command}} {{y:mv ../Eleanor .}}",
    ]
    counter = 0
    girl_file = os.path.join(HIDDEN_DIR, 'town/.hidden-shelter/Eleanor')

    def block_command(self, line):
        line = line.strip()
        if ("mv" in line or "cd" in line) and line not in self.command:
            if 'cd' in line:
                print 'Ability to Change Directory has been blocked'
            return True

    def check_command(self, line, current_dir):
        # Need to check if the girl is in the correct directory

        # strip any spaces off the beginning and end
        line = line.strip()

        if os.path.exists(self.girl_file) and self.counter < 1:
            return True
        # We can't verify the girl has been moved correctly at this step
        elif line.strip() in self.command and self.counter == 1:
            return True
        elif self.counter == 1:
            return True
        else:
            self.show_hint(line, current_dir)
            return False

    def show_hint(self, line, current_dir):
        hint = (
            "{{rn:Quick!  Use}} {{yb:mv ../Eleanor .}} "
            "{{rn:to move the little girl back to safety}}"
        )
        self.counter += 1
        self.send_hint(hint)

    def next(self):
        # if girl is saved
        if os.path.exists(self.girl_file):
            SaveGirl()

        else:
            copy_data(13, 1, 'a')
            play_sound('bell')
            LoseGirl()
