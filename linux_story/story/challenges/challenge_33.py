#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_34 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "Huh, you can't seem to look inside.",
        "It seems to be locked in the same way that library door was locked.",
        "Maybe there's a clue somewhere around here.",
        "{{lb:Investigate}} the area around and see if you can find any clues."
    ]
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing"

    # Level up based on the output of the command.

    hints = [
        "{{rb:Examine that signpost with}} {{yb:cat signpost}}{{rb:.}}"
    ]

    commands = [
        "cat signpost"
    ]

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?
    paired_hints = {
        "ls": "Try examining the individual items with {{lb:cat}}."
    }

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "So the signpost has an instruction on it? Let's carry it out.",
        "Use {{yb:./doorbell.sh}} to ring the doorbell."
    ]

    # It would be good if we could pass the current dir across and this would
    # simply be the default?
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhapes an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing"

    # Level up based on the output of the command.

    hints = [
        "{{rb:Use}} {{yb:./doorbell.sh}} {{rb:to ring the doorbell.}}"
    ]

    commands = [
        "./doorbell.sh"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Swordsmaster: WHO'S THERE",
        "",
        "1: ME",  # Reply with "Swordsmaster: I am also ME. I don't need to talk to any more MEs."
        "2: ",  # Username - this should pass
        "3: The one you want to speak to"  # "Swordsmaster: ...no, I don't think so.""
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo 2"
    ]

    def next(self):
        path = self.generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0755)
        NextStep(self.xp)
