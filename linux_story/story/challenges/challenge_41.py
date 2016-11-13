#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.challenges.challenge_42 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 41


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
        "Swordsmaster: {{Bb:You may need my help later. Come back if you are blocked "
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
        Step5(self.xp)


# The note should say:
# "There is a monster kidnapping people. I've been watching you, and think you
# could help. Find me, I'm deeper in the woods."
class Step5(StepTemplateChmod):
    story = [
        "It looks like we should go further into the woods.",
        "Let's leave the clearing and see where else we can go."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods"

    hints = [
        "{{rb:Go back to the woods with}} {{yb:cd ../}}"
    ]

    def block_command(self):
        unblock_cd_commands(self.last_user_input)

    def next(self):
        Step6()


# They'll find the rabbithole if they look more closely at this point.
class Step6(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "ls",
        "ls -a"
    ]
    story_dict = {
        "note_woods": {
            "path": "~/woods",
            "name": "note"
        }
    }

    # This text is used so much we can probably save it as "default ls hint"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateChmod):
    story = [
        "There's another note! Let's read it."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "cat note"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat note}} {{rb:to examine the note.}}"
    ]

    def next(self):
        Step8()


class Step8(StepTemplateChmod):
    story = [
        "Let's go into the thicket."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/thicket"
    hints = [
        "{{rb:Use}} {{yb:cd thicket}} {{rb:to go into the thicket.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step9()


class Step9(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    command = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    story_dict = {
        "note_thicket": {
            "path": "~/woods/thicket",
            "name": "note"
        }
    }

    def next(self):
        Step10()


class Step10(StepTemplateChmod):
    story = [
        "Yet another note, and a rabbithole. Will there be a bomb in this one?",
        "What does the note say?",
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "cat note"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    ]

    def next(self):
        NextStep(self.xp)
