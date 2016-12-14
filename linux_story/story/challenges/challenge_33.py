#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

# Redo chapter 5 with the swordmaster.

import os

from linux_story.Animation import Animation
from linux_story.common import get_story_file, get_username
from linux_story.helper_functions import wrap_in_box
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.challenges.challenge_41 import Step2 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands, unblock_commands


class StepTemplateNano(TerminalNano):
    challenge_number = 33


class StepTemplateChmod(TerminalChmod):
    challenge_number = 33


class Step1(StepTemplateNano):
    story = [
        "You hear a deep voice on the other side of the door.",
        "",
        "Swordmaster:",
        "{{Bb:If you have me, you want to share me.",
        "If you share me, you haven't got me.",
        "What am I?}}",
        "",
        "{{yb:1. What?}}",
        "{{yb:2. I don't know}}"
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
        "Swordmaster: {{Bb:I thought so. You need to complete the challenges}} {{lb:in the cave in the woods}}",
        "{{Bb:Come back when you've finished.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        "Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}",
        "{{yb:Head to}} {{bb:~/woods/cave}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo knock knock":
            self.send_hint("Swordmaster: {{Bb:Go and find the answer. Don't just stand there.}}")
            return
        return StepTemplateNano.check_command(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step2(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:That is not the answer! Find the answer}} {{lb:in the cave near the woods.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/cave"
    hints = [
        "Swordmaster: {{Bb:Head to the}} {{bb:~/woods/cave}} {{Bb:and stop hanging around outside my house!}}",
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
        "There are three rooms, a chest, and a couple of signs. {{lb:Read}} the two signs."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat r-sign"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = wrap_in_box([
        _("{{gb:New Spell:}} Type {{yb:chmod +r}} and press"),
        _("{{ob:Enter}} to {{lb:light up a dark room}}."),
    ])
    story += [
        "The sign suggests we should use this in the dark-room.",
        "First, {{lb:look in the dark-room}} to see why we need it."
    ]

    commands = [
        "ls dark-room",
        "ls dark-room/"
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    hints = [
        "Use {{yb:ls dark-room}} to look inside"
    ]

    def block_command(self):
        if "chmod +r" in self.last_user_input:
            return True
        return StepTemplateChmod.block_command(self)

    def check_command(self):
        if "chmod +r" in self.last_user_input:
            print "Before you run chmod, see what happens if you look in the dark room."
            return
        return StepTemplateChmod.check_command(self)

    def next(self):
        Step7()


# class Step6(StepTemplateChmod):
#     story = [
#         "Have a look around."
#     ]
#     start_dir = "~/woods/cave/dark-room"
#     end_dir = "~/woods/cave/dark-room"
#     commands = [
#         "ls",
#         "ls .",
#         "ls ./"
#     ]
#
#     def next(self):
#         Step7()


class Step7(StepTemplateChmod):
    story = [
        "You cannot see anything, because the lights are off",
        "To turn on the lights, {{lb:use the command you learnt.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +r dark-room",
        "chmod +r dark-room/"
    ]
    hints = [
        "Use {{yb:chmod +r dark-room}} to light up the dark-room."
    ]

    def next(self):
        Step8()


class Step8(StepTemplateChmod):
    story = [
        "Look inside the dark room again."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "ls dark-room",
        "ls ./dark-room",
        "ls ./dark-room/",
        "ls dark-room/",
    ]

    hints = [
        "Use {{yb:ls dark-room}} to look inside the dark-room"
    ]

    def next(self):
        Step9()


class Step9(StepTemplateChmod):
    story = [
        "You can see a set of {{lb:instructions}}. Read them."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat dark-room/instructions"
    ]

    hints = [
        "{{Bb:Use}} {{yb:cat dark-room/instructions}} to read the instructions"
    ]

    def next(self):
        Step10()


class Step10(StepTemplateChmod):
    story = [
        "The note says: {{lb:Move the lighter from the cage-room into the doorless-room.}}",
        "",
        "There is another room called {{bb:cage-room}}. Have a look inside."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    hints = [
        "Use the ls command to look inside the cage-room.",
        "{{rb:Use the command}} {{yb:ls cage-room}} {{rb:to look inside the cage-room.}}"
    ]
    commands = [
        "ls cage-room",
        "ls cage-room/"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step12()


# class Step11(StepTemplateChmod):
#     story = [
#         "Look around"
#     ]
#     start_dir = "~/woods/cave/cage-room"
#     end_dir = "~/woods/cave/cage-room"
#
#     commands = [
#         "ls"
#     ]
#
#     def next(self):
#         Step12()


class Step12(StepTemplateChmod):
    story = [
        "You see a bird, a lighter, and a w-sign.",
        "{{lb:Move}} the {{lb:lighter}} to {{lb:where you are}}."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage-room/lighter .",
        "mv cage-room/lighter ./",
        "mv cage-room/lighter doorless-room",
        "mv cage-room/lighter doorless-room/"
    ]

    hints = [
        "Use {{yb:mv cage-room/lighter .}} to move the lighter to where you are."
    ]

    optional_commands = {
        "cat cage-room/w-sign": False
    }

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def check_command(self):
        if self.last_user_input == "cat cage-room/bird":
            self.send_hint("The bird looks lifeless and unhappy.")
        elif self.last_user_input == "cat cage-room/lighter":
            self.send_hint("This must be the lighter the instructions in the dark-room was referring to")
        elif self.last_user_input == "cat cage-room/w-sign":
            self.optional_commands[self.last_user_input] = True;
            self.send_hint("To move the lighter.....does this mean you can't already? Try moving it.")
        return StepTemplateChmod.check_command(self)

    def next(self):
        if self.optional_commands["cat cage-room/w-sign"]:
            Step14()
        else:
            Step13()


class Step13(StepTemplateChmod):
    story = [
        "You are unable to move the lighter.",
        "Read the hint to see what's going on"
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat cage-room/w-sign"
    ]
    hints = ["Read the note using {{lb:cat cage-room/w-sign}}"]

    def next(self):
        Step14()


class Step14(StepTemplateChmod):
    story = wrap_in_box([
        _("{{gb:New Spell:}} Type {{yb:chmod +w}} and press"),
        _("{{ob:Enter}} to {{lb:unlock a cage}}."),
    ])
    story += [
        "Use {{yb:chmod +w cage-room}} unlock the cage."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +w cage-room",
        "chmod +w cage-room/"
    ]
    hints = ["Use {{yb:chmod +w cage-room}}"]

    def next(self):
        Step15()


class Step15(StepTemplateChmod):
    story = [
        "Move the lighter outside the cage-room to {{lb:where you are}}."
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "mv cage-room/lighter .",
        "mv cage-room/lighter ./"
    ]
    hints = [
        "Use {{yb:mv cage-room/lighter .}}"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step16()


class Step16(StepTemplateChmod):
    story = [
        "Tweet!",
        "",
        "The bird looks more alert.",
        "It flapped its wings and flew away!",
        "Press ENTER to continue"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"

    def next(self):
        Animation("bird-animation").play_across_screen(speed=10)
        Step17()


class Step17(StepTemplateChmod):
    story = [
        "It looks like the bird was trapped here.",
        "Look! It left a {{lb:scroll}} behind in the cage-room.",
        "Find and {{lb:examine}} the scroll to see what it says."
    ]

    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat cage-room/x-scroll"
    ]
    file_list = [
        {
            "contents": get_story_file("x-scroll"),
            "path": "~/woods/cave/cage-room/x-scroll",
            "permissions": 0644,
            "type": "file"
        }
    ]
    deleted_items = [
        "~/woods/cave/cage-room/bird"
    ]

    hints = [
        "Use {{yb:cat cage-room/x-scroll}}"
    ]

    def next(self):
        Step18()


# class Step17(StepTemplateChmod):
#     story = [
#         "Leave the cage room."
#     ]
#     start_dir = "~/woods/cave"
#     end_dir = "~/woods/cave"
#     commands = [
#         "cd ..",
#         "cd ../"
#     ]
#
#     def block_command(self):
#         return unblock_cd_commands(self.last_user_input)
#
#     def next(self):
#         Step18()


class Step18(StepTemplateChmod):
    story = [
        "{{lb:You cannot go into the doorless room..}}",
        "You're a stubborn individual, so you decide to try.",
        "Use {{yb:cd doorless-room}} to try and go inside the doorless room."
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
        "That didn't work.",
        "Use the {{yb:chmod +x doorless-room}} to get inside."
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
        "There is a firework, and an x-sign.",
        "Read the x-sign."
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "cat x-sign"
    ]

    def next(self):
        Step23()


class Step23(StepTemplateChmod):
    story = [
        "We need to move the lighter into this directory and activate it.",
        "First, {{lb:move the lighter from the parent directory .. to here .}}"
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"
    commands = [
        "mv ../lighter .",
        "mv ../lighter ./"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step24()


class Step24(StepTemplateChmod):
    story = [
        "Follow the {{lb:instructions}} to activate the lighter"
    ]

    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    commands = [
        "chmod +x lighter"
    ]

    hints = [
        "Look at the {{lb:instructions}} again if unsure",
        "Use {{yb:chmod +x lighter}} to {{lb:activate}} the lighter."
    ]

    def next(self):
        Step25()


class Step25(StepTemplateChmod):
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
        Step26()


class Step26(StepTemplateChmod):
    story = [
        "The lighter went {{gb:bright green}} after you activated it.",
        "Now use it with {{yb:./lighter}}"
    ]
    start_dir = "~/woods/cave/doorless-room"
    end_dir = "~/woods/cave/doorless-room"

    hints = "To use the lighter, "

    commands = [
        "./lighter"
    ]

    def next(self):
        Step26a()


class Step26a(StepTemplateChmod):
    story = [
        "You lit the firework!",
        "You know how to use the three chmod commands!",
        "",
        "Leave this room and go back into the cave",
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
        "There is a chest waiting for you. {{lb:It has all the permissions removed.}}",
        "Try and open it.",
        "{{lb:You need to combine the flags you learnt in the previous challenges.}}"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "chmod +rwx chest/"
    ]
    hints = [
        "Use {{yb:chmod +rwx chest/}} to unlock the chest."
    ]

    def next(self):
        Step28()


class Step28(StepTemplateChmod):
    story = [
        "{{gb:Well done!}} Look inside, and {{lb:examine}} the contents"
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/cave"
    commands = [
        "cat chest/answer"
    ]
    hints = [
        "Use {{yb:ls chest/}} to look inside the chest."
    ]

    def next(self):
        Step29()


class Step29(StepTemplateChmod):
    story = [
        "You've found the answer to the swordmaster's riddle!",
        "Now {{lb:go back to the swordmaster.}}",
        ""
    ]
    start_dir = "~/woods/cave"
    end_dir = "~/woods/clearing"
    hints = [
        "Head back to the {{lb:~/woods/clearing}} where the swordmaster lives"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step30()


class Step30(StepTemplateChmod):
    story = [
        "Knock on the swordmaster's door"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo knock knock"
    ]
    hints = [
        "Use {{yb:echo knock knock}} to knock on the swordmaster's door"
    ]

    def next(self):
        Step31()


class Step31(StepTemplateChmod):
    story = [
        "Swordmaster:",
        "{{Bb:If you have me, you want to share me.",
        "If you share me, you haven't got me.",
        "What am I?}}",
        "",
        "{{yb:1. A secret}}",
        "{{yb:2. I don't know}}",
        "",
        "Use {{lb:echo}} to reply."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "echo 1"
    ]
    hints = [
        "Swordmaster: {{lb:Incorrect. Did you finish the challenges in the cave? The answer was in there.}}"
    ]

    def next(self):
        path = self.generate_real_path("~/woods/clearing/house")
        os.chmod(path, 0755)
        Step32()


class Step32(StepTemplateChmod):
    story = [
        "{{wb:Cluck.}} {{gb:It sounds like the door unlocked.}}",
        "",
        "{{lb:Go in the house.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cd house}} {{rb:to go inside}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step33()


class Step33(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to go inside}}"
    ]
    commands = [
        "ls"
    ]

    def next(self):
        Step34()


class Step34(StepTemplateChmod):
    story = [
        "You see a Masked Swordmaster watching you.",
        "Listen to what he has to say."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cat swordmaster}} {{rb:to}} {{lb:listen}} "
        "{{rb:to what the swordmaster has to say.}}"
    ]
    commands = [
        "cat swordmaster"
    ]

    def next(self):
        Step35()


class Step35(StepTemplateNano):
    story = [
        "{{wb:Swordmaster:}} {{Bb:Child, why do you seek me?}}",
        "",
        "{{yb:1: I want to unlock the private section in the library.}}",
        "{{yb:2: Who are you?}}",
        "{{yb:3: Have you been leaving me the strange notes?}}",
        "",
        "Respond with {{yb:echo 1}}, {{yb:echo 2}}, or {{yb:echo 3}}."
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}}{{rb:.}}"
    ]
    extra_hints = {
        "echo 2": "Swordmaster: {{Bb:I am one who has removed themselves from society. The few who know of me call me the Masked Swordmaster.}}",
        "echo 3": "Swordmaster: {{Bb:What notes?}}"
    }

    last_step = True

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])
            return

        return StepTemplateNano.check_command(self)

    def next(self):
        Step36()


class Step36(StepTemplateChmod):
    print_text = [
        "{{yb:I want to unlock the private section in the library.}}"
    ]
    story = [
        "Swordmaster: {{Bb:Well, if you completed the challenges in the}} {{lb:~/woods/cave}}"
        "{{Bb:, then you already know how.}}",
        "{{Bb:A note of caution: what is inside is both powerful and dangerous.}}"
        "",
        "{{yb:1: What is inside that is so dangerous?}}",
        "{{yb:2: Why do you live so far from other people?}}",
        "{{yb:3: Do you know why people are disappearing?}}"
    ]

    commands = [
        "echo 3"
    ]
    # This logic for commands doesn't work
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    extra_hints = {
        "echo 1": "Swordmaster: {{Bb:A command that makes the wielder into a Super User and gives them tremendous power.}}",
        "echo 2": "Swordmaster: {{Bb:Being a swordmaster, I have the ability to}} {{lb:remove}} {{Bb:others. "
                  "This makes people uneasy around me, so I choose to live in the woods instead.}}"
    }

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            self.send_hint(self.extra_hints[self.last_user_input])

        return StepTemplateChmod.check_command(self)

    def next(self):
        Step37()


class Step37(StepTemplateNano):
    print_text = [
        "{{yb:Do you know why people are disappearing?}}"
    ]
    story = [
        "Swordmaster: {{Bb:I wasn't aware people were disappearing. Is that what is causing that bell sound?",
        "Perhaps it is good you are here then.",
        "Tell me, what is your name?}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "echo " + get_username()
    ]
    hints = [
        "Use {{yb:echo " + get_username() + "}} to give your name."
    ]

    def next(self):
        Step38()


class Step38(StepTemplateNano):
    story = [
        "Swordmaster: {{Bb:I thought you might be. Few have the power to use the commands you used earlier.",
        "How did I know your name? Use}} {{yb:ls -l}} {{Bb:to see.}}"
    ]
    commands = [
        "ls -l"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:ls -l}} {{Bb:}}"
    ]

    file_list = [
        {
            "contents": get_story_file("note_swordsmaster-house"),
            "path": "~/woods/clearing/house/note",
            "permissions": 0644,
            "type": "file"
        }
    ]

    def next(self):
        Step39()


class Step39(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Your name is written in this world, for anyone who knows where to look.}}",
        "{{Bb:...}}",
        "{{Bb:...why is there a}} {{lb:note}} {{in this room?}}",
        "{{Bb:Do you see it? Use}} {{lb:ls}} {{Bb:to see more clearly, and}} {{lb:read}} {{Bb:it to see what it says.}}"
    ]
    commands = [
        "cat note"
    ]

    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        NextStep()