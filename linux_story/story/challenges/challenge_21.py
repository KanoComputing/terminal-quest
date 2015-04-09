#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.Step import Step
from linux_story.step_helper_functions import unblock_command_list
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
# from linux_story.story.challenges.challenge_22 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 21

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Congratulations, you learnt the new skill mkdir!}}"
        "\nRuth: {{Bb:Awesome!  So you can help me build a shelter!",
        "Can we make it back at the barn?  Then it'll be easier to "
        "move the animals inside.}}",
        "\n{{gb:Go back into the barn}}"
    ]
    start_dir = "toolshed"
    end_dir = "barn"
    command = [
        "cd ../barn/",
        "cd ../barn"
    ]

    def block_command(self, line):
        return unblock_command_list(line, self.command)

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Now, I need this shelter to be hidden, "
        "something that people can't easily find.  Do you have "
        "any ideas of how to do that?}}"
    ]
    start_dir = "barn"
    end_dir = "barn"

    hint = [
        "To make something hidden, you need to put a dot . in front of the name",
        "Make a shelter called {{yb:.shelter}}. Remember the dot at the start!"
    ]

    def check_command(self, line, current_dir):
        # need to check if there is a directory made with a
        # dot in the front of the name
        pass

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        "Ruth: {{Bb:Did you make something? I can't see anything...",
        "Put me and the animals inside.  Please.}}"
    ]
    start_dir = "barn"
    end_dir = "barn"

    # need to specify the hint depending on what animal needs help next

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "{{gb:Congratulations!  You've saved the farm}}",
        "\nRuth: {{Bb:Thank you so much!  You've saved me "
        "and my animals.  I'm so grateful to everything you've done}}",
        "{{Bb:Do you think there are others like me, who could "
        "be stranded and in hiding?}}"
    ]


# Do we now go into town and help the people there?
