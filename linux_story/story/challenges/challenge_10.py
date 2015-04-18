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
from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_11 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(Step):
    challenge_number = 10

    def __init__(self, xp=""):
        Step.__init__(self, TerminalCd, xp)


# This is the difficult bit to get through
# In this level, try and find lots of corrupted ascii art around the kicthen?
# Or add pawprints?
# Encourage them to use cat in a few places

class Step1(StepTemplateCd):
    story = [
        "You're in your house.  You appear to be alone.",
        "Use {{yb:cat}} to have a look at some of the objects around you."
    ]
    allowed_commands = [
        "cat banana",
        "cat cake",
        "cat croissant",
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
            hint = (
                "\n{{gb:Well done!  Just look at}} {{yb:one}} "
                "{{gb:more item}}"
            )

        else:
            if self.first_time:
                hint = (
                    "{{ob:Look at two of the objects around you "
                    "using}} {{yb:cat}}"
                )
            else:
                hint = (
                    '{{rb:Use the command}} {{yb:' + self.allowed_commands[0] +
                    '}} {{rb:to progress}}'
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
        "There doesn't seem to be anything here but loads of food.",
        "See if you can find something back in {{yb:town}}.",
        "First, use {{yb:cd ..}} to leave the kitchen."
    ]
    start_dir = "kitchen"
    end_dir = "town"
    commands = [
        "cd ~/town",
        "cd ~/town/",
        "cd ..",
        "cd ../",
        "cd town",
        "cd town/",
        "cd ../..",
        "cd ../../",
        "cd"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def show_hint(self, line, current_dir):

        # decide command needed to get to next part of town
        if current_dir == 'kitchen' or current_dir == 'my-house':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd' or line == 'cd ../':
                hint = "{{gb:Good work!  Do it again!}}"

            # Otherwise, give them a hint
            else:
                hint = (
                    '{{rb:Use}} {{yb:cd ..}} {{rb:to make your way to town}}'
                )

        elif current_dir == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = (
                    "{{gb:Good work!  Now head to town with}} {{yb:cd town}}"
                )

            # Otherwise give them a hint
            else:
                hint = '{{rb:Use}} {{yb:cd town}} {{rb:to go into town}}'

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "Have another look around {{yb:ls}}",
    ]
    start_dir = "town"
    end_dir = "town"
    commands = "ls"
    hints = "{{rb:Use}} {{yb:ls}} {{rb:to have a look around the town}}"

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "The whole place appears to be deserted.",
        "However, you think you hear whispers.",
        # Make this writing small
        "\n{{Bn:\".....if they use}} {{yb:ls -a}}{{Bn:, they'll see us...\"}}",
        "{{Bn:\"..Shhh!  ...might hear....\"}}"
    ]
    start_dir = "town"
    end_dir = "town"
    commands = "ls -a"
    hints = [
        "{{rb:You heard whispers referring to}} {{yb:ls -a}}"
        "{{rb:, try using it!}}",
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
    commands = [
        "cd .hidden-shelter",
        "cd .hidden-shelter/"
    ]
    hints = [
        "{{rb:Try going inside the}} {{yb:.hidden-shelter}} {{rb:using }}"
        "{{yb:cd}}",
        "{{rb:Use the command}} {{yb:cd .hidden-shelter }}"
        "{{rb:to go inside}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Have a look around."
    ]
    start_dir = ".hidden-shelter"
    end_dir = ".hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to have a look around you}}"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
