#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.story.terminals.terminal_rm import TerminalRm


class StepTemplateRm(TerminalRm):
    challenge_number = 46


class Step1(StepTemplateRm):
    story = [
        "{{gb:Congratulations, you saved the all villagers.}}"
        "You are alone with the Rabbit and the bell.",
        "",
        "Time to end this."
    ]

    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]

    def check_command(self):
        
        return StepTemplateRm.check_command(self)

    def next(self):
        pass


