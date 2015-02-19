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
from linux_story.challenges.challenge_4.terminals import TerminalCd
from linux_story.challenges.challenge_6.steps import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_command_list


class StepTemplateCd(Step):
    challenge_number = 5

    def __init__(self):
        Step.__init__(self, TerminalCd)


class Step1(StepTemplateCd):
    story = [
        "{{gb:Congratulations, you earned 7 XP!}}\n",
        "{{wb:Mum:}} {{Bn:\"Hi sleepyhead, can you go and grab your Dad? "
        "Dinner is nearly ready. I think he's in the garden.\"}}\n",
        "Let's look for your Dad in the garden.",
        "First we need to leave the kitchen using {{yb:cd ..}}"
    ]
    start_dir = "kitchen"
    end_dir = "my-house"
    command = ""
    hints = "{{rb:To leave the kitchen, type}} {{yb:cd ..}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You are back in the main hall of your house",
        "Can you see your garden?  Have a look around you."
    ]
    start_dir = "my-house"
    end_dir = "my-house"
    command = "ls"
    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look around you}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "You see doors to the garden, your room and your parent's room.",
        "You want to go into your {{yb:garden}}"
    ]
    start_dir = "my-house"
    end_dir = "garden"
    command = ""
    hints = "{{rb:Type}} {{yb:cd garden}} {{rb:to go into the garden}}"

    def block_command(self, line):
        allowed_commands = ["cd garden", "cd garden/"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Use {{yb:ls}} to look in the garden for your Dad."
    ]
    start_dir = "garden"
    end_dir = "garden"
    command = "ls"
    hints = (
        "{{rb:To look for your Dad, type}} {{yb:ls}} {{rb:and press "
        "Enter}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "The garden is well tended and the flowers are in bloom.",
        "Hmmm... you can't see him anywhere.",
        "Maybe he's in the {{yb:greenhouse}}. Go into the greenhouse."
    ]
    start_dir = "garden"
    end_dir = "greenhouse"
    command = ""
    hints = "{{rb:To go to the greenhouse, type}} {{yb:cd greenhouse}}"

    def block_command(self, line):
        allowed_commands = ["cd greenhouse", "cd greenhouse/"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Is he here? Type {{yb:ls}} to find out."
    ]
    start_dir = "greenhouse"
    end_dir = "greenhouse"
    command = "ls"
    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look for your Dad.}}"

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
        "Your dad has been busy, there are loads of vegetables here.",
        "Hmmmm. He's not here. But there is something odd.",
        "You see a note on the ground.  Use {{yb:cat note}} to read what "
        "it says"
    ]
    start_dir = "greenhouse"
    end_dir = "greenhouse"
    command = "cat note"
    hints = "{{rb:Type}} {{yb:cat note}} {{rb:to see what the note says!}}"

    def next(self):
        Step8()


class Step8(StepTemplateCd):
    story = [
        "Going back is super easy. Just type {{yb:cd ..}} to go back the way "
        "you came."
    ]
    start_dir = "greenhouse"
    end_dir = "garden"
    command = ""
    hints = "{{rb:Type}} {{yb:cd ..}} {{rb:to go back to the garden}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step9()


class Step9(StepTemplateCd):
    story = [
        "You're back in the garden.  Use {{yb:cd ..}} again to go back to "
        "the house."
    ]
    start_dir = "garden"
    end_dir = "my-house"
    command = ""
    hints = "{{rb:Type}} {{yb:cd ..}} {{rb:to go back to the house}}"

    def block_command(self, line):
        allowed_commands = ["cd ..", "cd ../"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        Step10()


class Step10(StepTemplateCd):
    story = [
        "Head back into the kitchen"
    ]
    start_dir = "my-house"
    end_dir = "kitchen"
    command = ""
    hints = "{{rb:Type}} {{yb:cd kitchen}} {{rb:to go back to the kitchen}}"

    last_step = True

    def block_command(self, line):
        allowed_commands = ["cd kitchen", "cd kitchen/"]
        return unblock_command_list(line, allowed_commands)

    def next(self):
        NextChallengeStep()
