#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.Step import Step
from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.challenges.challenge_11.steps import Step1 as NextStep


class StepTemplateCd(Step):
    challenge_number = 10

    def __init__(self):
        Step.__init__(self, TerminalCd)


############################################################################
# This is the difficult bit to get through
# In this level, try and find lots of corrupted ascii art around the kicthen?
# Or add pawprints?
# Encourage them to use cat in a few places

class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 25 XP!}}\n",
        "You're in your house.  You appear to be alone.",
        "Use {{yb:cat}} to have a look at some of the objects around you."
    ]
    allowed_commands = [
        "cat banana",
        "cat cake",
        "cat crossaint",
        "cat grapes",
        "cat milk",
        "cat newspaper",
        "cat oven",
        "cat pie",
        "cat sandwich",
        "cat table"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    counter = 0
    first_time = True

    def check_command(self, line, current_dir):
        line = line.strip()

        if line in self.allowed_commands:
            self.counter += 1
            self.allowed_commands.remove(line)
            hint = "\n{{gb:Congratulations!  Just look at one more item}}"

        else:
            if self.first_time:
                hint = (
                    "{{r:Look at two of the objects using}} {{yb:cat}} "
                    "{{rn:to see if you can find any clues}}"
                )
            else:
                hint = (
                    '{{r:Try the command}} {{yb:' + self.allowed_commands[0] + '}} '
                    '{{rn:to progress}}'
                )

        level_up = (self.counter >= 2)

        if not level_up:
            self.send_hint(hint)
            self.first_time = False
        else:
            return level_up

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "There seems to be nothing here but loads of food.",
        "See if you can find something outside the house"
    ]
    start_dir = "kitchen"
    end_dir = "town"
    command = ""
    hints = [
        "{{r:See if there is anything back in the town}}",
        "{{r:Use}} {{yb:cd}} {{rn:to get back into town}}"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        allowed_commands = [
            "cd ~/town",
            "cd ~/town/",
            "cd ..",
            "cd ../",
            "cd town",
            "cd town/",
            "cd ../..",
            "cd ../../"
        ]

        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def show_hint(self, line, current_dir):

        # decide command needed to get to next part of town
        if current_dir == 'kitchen' or current_dir == 'my-house':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd' or line == 'cd ../':
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise, give them a hint
            else:
                hint = '{{r:Use}} {{yb:cd ..}} {{rn:to make your way to town}}'

        elif current_dir == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = "{{gb:Good work!  Keep going!}}"

            # Otherwise give them a hint
            else:
                hint = '{{r:Use}} {{yb:cd town}} {{rn:to go into town}}'

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        Step3()


############################################################################


class Step3(StepTemplateCd):
    story = [
        "Have a look around",
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls"
    hints = "{{r:Use}} {{yb:ls}} {{rn:to have a look around the town}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "You can't see much here.  The place appears to be deserted.",
        "However, you think you hear whispers.",
        # Make this writing small
        "{{wn:\".....if they use}} {{yb:ls -a}}{{wn:, they'll see us...\"}}",
        "{{wn:\"..Shhh!  ...might hear....\"}}"
    ]
    start_dir = "town"
    end_dir = "town"
    command = "ls -a"
    hints = [
        "{{r:You heard whispers referring to}} {{yb:ls -a}}"
        "{{r:, try using it!}}",
    ]

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "You see a {{yb:.hidden-shelter}} that you didn't notice before.",
        "It sounds like the whispers are coming from there.  Try going in."
    ]
    start_dir = "town"
    end_dir = ".hidden-shelter"
    command = ""
    hints = [
        "{{r:Try going inside the}} {{yb:.hidden-shelter}} {{rn:using }}"
        "{{yb:cd}}",
        "{{r:Use the command}} {{yb:cd .hidden-shelter }}"
        "{{rn:to go inside}}"
    ]

    def block_command(self, line):
        allowed_commands = [
            "cd .hidden-shelter",
            "cd .hidden-shelter/"
        ]

        line = line.strip()
        if "cd" in line and line not in allowed_commands:
            return True

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Have a look around."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{r:Use}} {{yb:ls}} {{r:to have a look around you}}"
    ]

    def next(self):
        NextStep()
