#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_nano import TerminalNano
# from linux_story.story.challenges.challenge_26 import Step1 as NextChallengeStep


# Test chapter
class StepTemplateNano(TerminalNano):
    challenge_number = 25


class TerminalNanoMod(TerminalNano):

    def do_nano(self, line):
        self.send_text("\n{{gb:You've opened nano!  Now type}} {{lb:hello}}")
        TerminalNano.do_nano(self, line)


class Step1(StepTemplateNano):
    story = [
        "First use the command {{yb:nano}} and press Enter."
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    finished_level = False
    end_text = "hello"
    end_filename = "filename.txt"
    start_nano = 0
    hints = [
        "{{rb:Try typing}} {{yb:nano}} {{rb:and pressing Enter.}}"
    ]

    def check_command(self, line, current_dir):
        end_path = os.path.join(
            os.path.expanduser("~"),
            ".linux-story/farm/barn/filename.txt"
        )

        if os.path.exists(end_path):
            # check contents of file contains the self.end_text
            f = open(end_path, "r")
            text = f.read()
            f.close()

            if text.strip() == self.end_text:
                # self.send_text(
                #    "\n{{gb:Congratulations, you used nano correctly!}}"
                # )
                return self.finish_if_server_ready(True)

    def check_nano_content(self):
        '''Have a similar system as with block_command and check_command

        Stages we need to achieve:

        ALREADY CREATED FILE:
        - check they open the correct file
        - check the user types the correct text into the file, on the right
          line
        - prompt the user to save (Ctrl X)
        - check the user did save it correctly (did not cancel before saving.)

        NEW FILE:
        - open new file
        - check the user types the correct text into the file, on the right
          line
        - prompt the user to save (Ctrl X)
        - Check they enter the correct filename at this point.
        - check the user did save it correctly (did not cancel before saving.)

        - double check: after the process, check the file exists and the text
          inside is correct.

        The two outlines above are pretty generic, so many try and make it
        more generic

        '''
        # Make the if statements cumulative, so you trickle down as less
        # conditions are satisfied.

        if not self.get_nano_running():
            if self.get_nano_filename() == self.end_filename:
                return True
            else:
                self.send_text(
                    "\n{{ob:Your filename is wrong. Try starting again by "
                    "typing}} {{yb:nano}} {{ob:and press Enter}}"
                )

        elif self.get_on_filename_screen() and \
                self.get_nano_content().strip() == self.end_text:
            self.send_text(
                "\n{{gb:Type}} {{yb:filename.txt}} {{gb:and press}} "
                "{{yb:Enter}}"
            )

        elif self.get_on_filename_screen():
            self.send_text(
                "\n{{ob:Oops, your text isn't correct. Press}} "
                "{{yb:Ctrl C}} {{ob:to cancel.}}"
            )

        elif self.get_save_prompt_showing():
            self.send_text(
                "\n{{gb:Press}} {{yb:Y}} {{gb:to confirm that you want to "
                "save.}}"
            )

        elif self.get_nano_content().strip() == self.end_text:
            self.send_text(
                "\n{{gb:Excellent, you typed hello. Now press}} "
                "{{yb:Ctrl X}} {{gb:to exit.}}"
            )

        return False

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "{{gb:You've finished the challenge!}}"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    def next(self):
        pass
