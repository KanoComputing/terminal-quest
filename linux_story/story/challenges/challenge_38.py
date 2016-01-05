#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands, unblock_commands_with_mkdir_hint
)
from linux_story.story.challenges.challenge_39 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 38


class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:There's a note that's appeared. Who left it here?",
        "...this is very strange. I left the door open. Perhaps someone...or "
        "something...sneaked in while we were training.}}",
        "",
        "{{Bb:What does it say?}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cat note"
    ]

    hints = [
        "{{rb:Read the note with}} {{yb:cat note}}"
    ]

    def next(self):
        Step2()


# Note is from the rabbit and says "It's time for us to meet.
# Follow the notes to find me."
class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:I see you are involved in something bigger than I "
        "thought.",
        "You may need my help later. Remember me if you find you are blocked "
        "by lack of knowledge.}}",
        "",
        "Time to head off - leave the swordsmaster's house."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing"

    hints = [
        "{{rb:Leave the house and go into the clearing with}} {{yb:cd ..}}"
    ]

    # this should be inherited somehowz
    def block_command(self):
        unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Look around and see if there are clues about where to go next."
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    story_dict = {
        "note_swordsmaster-clearing": {
            "path": "~/woods/clearing",
            "name": "note"
        }
    }

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Another one! What does this say?"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "cat note"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    ]

    def next(self):
        NextStep(self.xp)
