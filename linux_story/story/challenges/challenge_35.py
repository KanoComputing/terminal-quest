#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands, unblock_commands_with_cd_hint
)
from linux_story.story.challenges.challenge_36 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 35


class StepTemplateChmod(TerminalChmod):
    challenge_number = 35


# Instead of a sandwich, make this a script, and then the last task is to make
# it executable.
class Step1(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Well done. You've made the basement readable, "
        "and you can see there is a}} {{lb:key.sh}} {{Bb:in there.}}",
        "{{Bb:Now try and move the}} {{lb:key.sh}} {{Bb:into the parent "
        "directory ../}}"
    ]
    commands = [
        "mv sandwich ../",
        "mv sandwich .."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:mv sandwich ../}} {{rb:to move the sandwich "
        "out of the basement.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step9()


class Step9(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now you get the error}} {{yb:mv: cannot move "
        "sandwich to ../sandwich: Permission denied}}",
        "{{Bb:This is because you do not have Write Access to this directory.",
        "To give yourself this, use}} {{yb:chmod +w ./}}."
    ]
    commands = [
        "chmod +w ./",
        "chmod +w ."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Use}} {{yb:chmod +w ./}} {{rb:to make the current directory "
        "Writeable}}"
    ]

    def next(self):
        Step10()


class Step10(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now try again. Fetch the}} {{lb:sandwich}}{{Bb:.}}"
    ]
    commands = [
        "mv sandwich ../",
        "mv sandwich .."
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    commands = [
        "mv sandwich ../",
        "mv sandwich .."
    ]

    hints = [
        "{{rb:Use}} {{yb:mv sandwich ../}} {{rb:to move the sandwich}} "
        "{{rb:back a directory.}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step11()


class Step11(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Thank you, I was hungry.}}",
        "The swordsmaster calmly eats the sandwich.",
        "Swordsmaster: {{Bb:Well done - you've learned to use chmod.}}",
        "{{Bb:...}}",
        "{{Bb:...wait, what is this?}}",
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
    deleted_items = [
        "~/woods/clearing/house/sandwich"
    ]

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step12()


class Step12(StepTemplateChmod):
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
        Step13()


# Note is from the rabbit and says "It's time for us to meet.
# Follow the notes to find me."
class Step13(StepTemplateChmod):
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
        Step14()


class Step14(StepTemplateChmod):
    story = [
        "Look around and see if there are any other notes around."
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]

    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb: to look around.}}"
    ]
    story_dict = {
        "note_swordsmaster-clearing": {
            "path": "~/woods/clearing",
            "name": "note"
        }
    }

    def next(self):
        Step15()


class Step15(StepTemplateChmod):
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
        Step16()


# The note should say:
# "There is a monster kidnapping people. I've been watching you, and think you
# could help. Find me, I'm deeper in the woods."
class Step16(StepTemplateChmod):
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
        Step17()


# They'll find the rabbithole if they look more closely at this point.
class Step17(StepTemplateChmod):
    story = [
        "Look around"
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
        Step18()


class Step18(StepTemplateChmod):
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
        Step19()


class Step19(StepTemplateChmod):
    story = [
        "Go deeper into the woods...so let's go!"
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/thicket"
    hints = [
        "{{rb:Use}} {{yb:cd thicket}} {{rb:to go deeper.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step20()


class Step20(StepTemplateChmod):
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
        Step21()


class Step21(StepTemplateChmod):
    story = [
        "Yet another note...let's read this one.",
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
