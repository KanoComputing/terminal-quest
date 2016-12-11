#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from linux_story.Animation import Animation
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_34 import Step1 as NextStep, StepTemplateChmod
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "You hear a deep voice on the other side of the door.",
        "",
        "Swordmaster: {{Bb:If you have me, you want to share me. If you share me, you haven't got me. What am I?}}",
        "",
        "{{yb:1. I don't know?}}",
        "{{yb:2. What?}}"
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        if self.last_user_input.lower() == "secret" or self.last_user_input.lower() == "echo secret":
            Step1b()
        else:
            Step2()


class Step1b(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:...Did you complete the cave challenge?",
        "Fine, here's another. Unlock the door to my house.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    def next(self):
        Step1c()


class Step1c(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:I thought so. You need to complete the challenges in the cave in the woods. Come back when "
        "you've finished.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"

    def check_command(self):
        if self.last_user_input == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there.}}")

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step2(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:That is not the answer! You can try and find the answer to the riddle in cave near the woods.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        "Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging about outside my house!}}",
        "{{yb:Head to}} {{bb:~/woods/cave}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there guessing.}}")
            return
        return StepTemplateNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "There are three rooms, and a sign. {{lb:Read}} the sign."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat sign"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    # the sign should read:
    # Three rooms, each with a permission missing.
    # Start with the dark room. To switch on the lights, use chmod +r
    story = [
        "So you have the command chmod +r. What does it do?",
        "To find out, {{lb:go into the dark room}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave/dark-room"

    hints = [
        "Use {{yb:cd dark-room}} to go inside"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "Have a look around."
    ]
    start_dir = "~/woods/cave/dark-room"
    end_dir = "~/woods/cave/dark-room"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateChmod):
    story = [
        "The lights in this room are off. Try using the command you read on the sign."
        # add new spell here of chmod +r
    ]
    start_dir = "~/woods/cave/dark-room"
    end_dir = "~/woods/cave/dark-room"
    commands = [
        "chmod +r ./",
        "chmod +r ."
    ]
    hints = [
        "Use {{yb:chmod +r .}}"
    ]

    def next(self):
        Step8()


class Step8(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/cave/dark-room"
    end_dir = "~/woods/cave/dark-room"
    commands = [
        "ls",
        "ls .",
        "ls ./",
    ]

    hints = [
        "{{Use}} {{yb:ls}}"
    ]

    def next(self):
        Step9()


class Step9(StepTemplateChmod):
    story = [
        "You can see a set of {{lb:instructions}}. Read it."
    ]
    start_dir = "~/woods/cave/dark-room"
    end_dir = "~/woods/cave/dark-room"
    commands = [
        "cat instructions"
    ]

    hints = [
        "{{Bb:Use}} {{yb:cat instructions}}"
    ]

    def next(self):
        Step10()


class Step10(StepTemplateChmod):
    # The note should read:
    # Move the lighter from the cage into the doorless room.
    # When the bird is free, you will be able to progress.
    # You'll need chmod +w
    story = [
        "The note refers to the cage. Let's go over there."
    ]
    start_dir = "~/woods/cave/dark-room"
    end_dir = "~/woods/cave/cage-room"
    hints = [
        "{{rb:Go into the cage room using cd.}}",
        "{{rb:Use the command}} {{yb:cd ../cage}} {{rb:to go inside the cage.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step11()


class Step11(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"

    commands = [
        "ls"
    ]

    def next(self):
        Step12()


class Step12(StepTemplateChmod):
    story = [
        "You see a bird, a lighter, and a note.",
        "This must be the lighter the note in the dark room was referring to.",
        "Move it outside this room, to .."
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"
    commands = [
        "mv lighter ..",
        "mv lighter ../",
        "mv lighter ../doorless-room",
        "mv lighter ../doorless-room/"
    ]

    hints = [
        "Use mv lighter ../doorless-room"
    ]

    optional_commands = {
        "cat note": False
    }

    def check_command(self):
        if self.last_user_input == "cat bird":
            self.send_hint("The bird looks lifeless and unhappy.")
        elif self.last_user_input == "cat lighter":
            self.send_hint("This must be the lighter the instructions in the dark-room was referring to")
        elif self.last_user_input == "cat note":
            self.optional_commands[self.last_user_input] = True;
            self.send_hint("To move the lighter.....does this mean you can't already? Try moving it.")

    def next(self):
        if self.optional_commands["cat note"]:
            Step14()
        else:
            Step13()


class Step13(StepTemplateChmod):
    story = [
        "You are unable to move the lighter.",
        "Read the note to see what's going on"
    ]

    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"
    commands = [
        "cat note"
    ]
    hints = ["Read the note using {{lb:cat note}}"]

    def next(self):
        Step14()


class Step14(StepTemplateChmod):
    # The note should say something like
    story = [
        "So you are unable to move the lighter because the write permissions are removed from the room.",
        "Add them with chmod +w ."
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"
    commands = [
        "chmod +w ./",
        "chmod +w ."
    ]
    hints = ["Use chmod +w ."]

    def next(self):
        Step15()


class Step15(StepTemplateChmod):
    story = [
        "Tweet!",
        "",
        "The bird looks more alert.",
        "It flapped its wings and flew away!",
        "Press ENTER to continue"
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"

    def next(self):
        Animation("bird").play_across_screen(speed=10)
        Step16()


class Step16(StepTemplateChmod):
    story = [
        "It looks like the bird was trapped here.",
        "Try and move the note out of here and into the doorless-room"
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave/cage-room"
    commands = [
        "mv lighter ../doorless-room",
        "mv lighter ../doorless-room/"
    ]
    hints = [
        "Use mv lighter ../doorless-room"
    ]

    def next(self):
        Step17()


class Step17(StepTemplateChmod):
    story = [
        "Leave the cage room."
    ]
    start_dir = "~/woods/cave/cage-room"
    end_dir = "~/woods/cave"
    commands = [
        "cd ..",
        "cd ../"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step18()


class Step18(StepTemplateChmod):
    story = [
        "The final room is the doorless room.",
        "Try and go inside."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    dirs_to_attempt = "~/woods/cave/doorless-room"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step19()


class Step19(StepTemplateChmod):
    story = [
        "You don't see a way in, and cannot go inside.",
        "What did the note say from the cage room?",
        "Use the chmod +x ./ to get inside"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    commands = [
        "chmod +x doorless-room",
        "chmod +x doorless-room/"
    ]

    def next(self):
        Step20()


class Step20(StepTemplateChmod):
    story = [
        "Now try and go inside."
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave/doorless-room"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step21()


class Step21(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "ls"
    ]

    def next(self):
        Step22()


class Step22(StepTemplateChmod):
    story = [
        "There is a firework, lighter and a final set of instructions.",
        "Go and read the set of instructions."
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "cat instructions"
    ]

    def next(self):
        Step23()


class Step23(StepTemplateChmod):
    story = [
        "Follow the instructions to activate the lighter"
    ]

    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "chmod +x lighter"
    ]

    def next(self):
        Step24()


class Step24(StepTemplateChmod):
    story = [
        "Look around to see what happened to the lighter"
    ]

    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step25()


class Step25(StepTemplateChmod):
    story = [
        "The lighter went bright green after you activated it.",
        "Now use it with {{yb:./lighter}}"
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "./lighter"
    ]

    def next(self):
        Step26()


class Step26(StepTemplateChmod):
    story = [
        "You lit the firework!",
        "You know how to use the three chmod commands"
        "Leave the room and go back into the cave",
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step27()


class Step27(StepTemplateChmod):
    story = [
        "Time to face the final hurdle.",
        "There is a chest waiting for you.",
        "Try and open it."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +rwx chest/"
    ]


    def next(self):
        pass