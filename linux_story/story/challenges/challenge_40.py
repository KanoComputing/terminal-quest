#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_41 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 40


class Step1(StepTemplateChmod):
    story = [
        # This wraps very early
        "Swordsmaster: {{Bb:Well done, you've learned how give yourself three permissions.}}",
        "{{lb:Read}}",
        "{{lb:Write}}",
        "{{lb:Execute}}",
        "{{Bb:Come out of there and I will show you one final thing.}}"
    ]
    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cd ..",
        "cd ../"
    ]
    hints = [
        "Use cd .. to leave"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You learnt how to grant yourself individual permissions. However you can also combine "
        "them and use them all at once. If you use}} {{lb:chmod +rwx}} {{Bb:you can unlock them all in one go.}}",
        "{{Bb:Try it out on the fo}}"
    ]

    start_dir = "~/woods/clearing/house/no-entry-room"
    end_dir = "~/woods/clearing/house/no-entry-room"
    commands = [
    ]
    hints = [
        "Nada"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Thank you, you locked the basement back up for me.}}",
        "{{Bb:Well done - you've learned to use chmod!}}",
        "{{Bb:...}}",
        "{{Bb:...}}",
        "{{Bb:...what is this?}}",
        "{{Bb:Do you see this? Have a}} {{lb:look around}}."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "ls",
        "ls -a"
    ]

    story_dict = {
        "note_swordsmaster-house": {
            "path": "~/woods/clearing/house",
            "name": "note"
        }
    }

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        NextStep()
