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
from linux_story.story.challenges.challenge_6 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(Step):
    challenge_number = 5

    def __init__(self, xp=""):
        Step.__init__(self, TerminalCd, xp)


class Step1(StepTemplateCd):
    story = [
        "{{wb:Mum:}} {{Bb:\"Hi sleepyhead, breakfast is nearly ready. "
        " Can you go and grab your Dad?"
        " I think he's in the garden.\"}}\n",
        "Let's look for your Dad in the garden.",
        "First we need to leave the kitchen using {{yb:cd ../}}\n"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:To leave the kitchen, type}} {{yb:cd ../}}"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        "You are back in the main hall of your house.",
        "Can you see your garden?  Have a look around you.\n"
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house"
    commands = "ls"
    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look around you}}"

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        "You see doors to the {{bb:garden}}, {{bb:kitchen}}, "
        "{{bb:my-room}} and {{bb:parents-room}}.",
        "Head into your {{lb:garden}}.\n"
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house/garden"
    commands = ["cd garden", "cd garden/"]
    hints = "{{rb:Type}} {{yb:cd garden/}} {{rb:to go into the garden.}}"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        "Use {{yb:ls}} to look in the garden for your Dad.\n"
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house/garden"
    commands = "ls"
    hints = (
        "{{rb:To look for your Dad, type}} {{yb:ls}} {{rb:and press "
        "Enter.}}"
    )

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        "The garden looks beautiful at this time of year.",
        "Hmmm...but you can't see him anywhere.",
        "Maybe he's in the {{lb:greenhouse}}. Go inside the greenhouse.\n"
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house/garden/greenhouse"
    commands = ["cd greenhouse", "cd greenhouse/"]
    hints = "{{rb:To go to the greenhouse, type}} {{yb:cd greenhouse/}}"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        "Is he here? Type {{yb:ls}} to find out.\n"
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden/greenhouse"
    commands = "ls"
    hints = "{{rb:Type}} {{yb:ls}} {{rb:to look for your Dad.}}"

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
        "Your dad has been busy, there are loads of vegetables here.",
        "Hmmmm. He's not here. But there is something odd.",
        "You see a note on the ground.  Use {{yb:cat note}} to read what "
        "it says.\n"
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden/greenhouse"
    commands = "cat note"
    hints = "{{rb:Type}} {{yb:cat note}} {{rb:to see what the note says!}}"

    def next(self):
        Step8()


class Step8(StepTemplateCd):
    story = [
        "Going back is super easy. Just type {{yb:cd ../}} to go back the way "
        "you came.\n"
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:Type}} {{yb:cd ../}} {{rb:to go back to the garden.}}"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step9()


class Step9(StepTemplateCd):
    story = [
        "You're back in the garden. Use {{yb:cd ../}} again to"
        " go back to the house.",
        "{{gb:Top tip: Press the UP arrow key to replay your previous command.}}\n"
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house"
    commands = ["cd ..", "cd ../"]
    hints = "{{rb:Type}} {{yb:cd ../}} {{rb:to go back to the house.}}"

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step10()


class Step10(StepTemplateCd):
    story = [
        "Now go back into the {{lb:kitchen}} and see Mum.\n"
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house/kitchen"
    commands = ["cd kitchen", "cd kitchen/"]
    hints = "{{rb:Type}} {{yb:cd kitchen/}} {{rb:to go back to the kitchen.}}"

    last_step = True

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        NextChallengeStep(self.xp)
