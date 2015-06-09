#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano_step import TerminalNano
# from linux_story.story.challenges.challenge_21 import Step1 as NextChallengeStep


# Test chapter
class StepTemplateNano(TerminalNano):
    challenge_number = 26


class Step1(StepTemplateNano):
    story = [
        "hello"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    def finished_challenge(self):
        return self.check_nano_output()

    def check_nano_content(self, nano_content):
        '''Have a similar system as with block_command and check_command

        Stages we need to achieve:

        ALREADY CREATED FILE:
        - check they open the correct file
        - check the user types the correct text into the file, on the right line
        - prompt the user to save (Ctrl X)
        - check the user did save it correctly

        NEW FILE:
        - open new file
        - check the user types the correct text into the file, on the right line
        - prompt the user to save (Ctrl X)
        - Check they enter the correct filename at this point.
        - check the user did save it correctly (did not cancel before saving.)

        - double check: after the process, check the file exists and the text inside is correct.
        '''

        if nano_content == "hello alejandro":
            self.send_text("\n{{gb:Congratulations}}")
            return True

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Congratulations"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    def next(self):
        pass
