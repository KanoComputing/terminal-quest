#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_22 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 21

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Nice! You learned the new skill - mkdir!}}",
        "\nRuth: {{Bb:Awesome!  So you can help me build a shelter!",
        "Can we make it back at the barn?  Then it'll be easier to "
        "move the animals inside.}}",
        "\n{{yb:Go back into the barn}}"
    ]
    start_dir = "toolshed"
    end_dir = "barn"
    commands = [
        "cd ../barn/",
        "cd ../barn"
    ]
    hints = [
        "{{rb:Go back to the barn in one step by going back "
        "a directory first. Try using}} "
        "{{yb: cd ../barn}}"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Anyone can find the igloo though, "
        "can we make something that people can't find. Do you have "
        "any ideas how we can make a hidden shelter?}}",
        "\nTo make something hidden, you need to put a dot . in front of the "
        "name.",
        "Make a shelter called {{yb:.shelter}}. Remember the dot at the start!"
    ]
    start_dir = "barn"
    end_dir = "barn"

    hint = [
        "{{rb:Make a shelter called}} {{yb:.shelter}}{{rb:. Remember the dot at the start!}}"
    ]

    def block_command(self, line):
        line = line.strip()
        if line.startswith("mkdir ."):
            return False
        else:
            return True

    def check_command(self, line, current_dir):
        # check files in the toolshed directory
        pass

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "Check it is properly hidden. Use {{yb:ls}} to "
        "see if it is visible.",
    ]

    commands = [
        "ls"
    ]

    def check_command(self, line, current_dir):
        line = line.strip()
        if line == "ls -a":
            self.send_hint(
                "{{rb:Use}} {{yb:ls}} {{rb:instead of}} {{yb:ls -a}} "
                "{{yb:to check that you can't see it}}"
            )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Now look around with {{yb:ls -a}} to check it actually exists!"
    ]
    start_dir = "barn"
    end_dir = "barn"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb:to look around}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Did you make something? That's amazing! "
        "Unfortunately I can't see it...please can you put me ",
        "and the animals inside?}}"
    ]
    start_dir = "barn"
    end_dir = "barn"
    commands = [
        "mv Trotter .shelter",
        "mv Trotter .shelter/",
        "mv Daisy .shelter",
        "mv Daisy .shelter/",
        "mv Cobweb .shelter",
        "mv Cobweb .shelter/"
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    # move the animals in one by one

    def next(self):
        NextChallengeStep(self.xp)
