#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.Animation import Animation
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands, unblock_commands
from linux_story.story.challenges.challenge_38 import Step1 as NextStep


def tweet_bird(callback, step_, user_input):
    if user_input == "cat bird":
        # play cheep noise.
        callback("\nBird: {{Bb:Tweet!}}")
        return
    return StepTemplateChmod.check_command(step_)


class StepTemplateChmod(TerminalChmod):
    challenge_number = 37


class Step1(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Well done. Your next challenge is in the}} {{bb:cage-room}}",
        "{{lb:Go inside}}."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "cd cage-room",
        "cd cage-room/"
    ]
    hints = [
        "Swordmaster: {{Bb:Do you remember how to go inside? Use}} {{yb:cd cage-room}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Look around.}}"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "ls"
    ]
    hints = [
        "Use {{yb:ls}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    # play cheep noise.
    story = [
        "There's a bird inside."
        "",
        "Swordmaster: {{Bb:To demonstrate what is special about this room, try and set the bird free by}} "
        "{{lb:moving it outside the current room}}"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    hints = [
        "Swordmaster: {{Bb:You want to move the bird to the directory}} {{yb:../}}",
        "Swordmaster: {{rb:Use}} {{yb:mv bird ../}} {{rb:to move the bird outside the room.}}"
    ]
    commands = [
        "mv bird ../",
        "mv bird .."
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def check_command(self):
        if self.last_user_input == "cat bird":
            # play cheep noise.
            self.send_hint("\nBird: {{Bb:Tweet!}}")
            return
        return StepTemplateChmod.check_command(self)

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:That didn't work. The bird can't escape, as the cage-room has had its}} {{lb:write}} "
        "{{Bb:permissions removed.}}",
        "{{Bb:To return the write permissions to this current room, use}} {{yb:chmod +w .}}"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    commands = [
        "chmod +w .",
        "chmod +w ./"
    ]
    hints = [
        "Swordmaster: {{rb:Use}} {{yb:chmod +w .}} {{rb:to return the write permissions.}}"
    ]

    def check_command(self):
        if self.last_user_input == "cat bird":
            self.send_hint("\nBird: {{Bb:Tweet!}}")
            return
        if self.last_user_input == "chmod +w":
            self.send_hint("\nSwordmaster: {{Bb:The command is}} {{yb:chmod +w .}} {{Bb:- don't forgot the dot!}}")
            return
        return StepTemplateChmod.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Now you should be able to release the bird. Use}} {{lb:mv}} {{Bb:to release the bird.}}"
    ]
    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house/cage-room"
    hints = [
        "Swordmaster: {{Bb:You want to move the bird to the directory}} {{yb:../}}",
        "Swordmaster: {{rb:Use}} {{yb:mv bird ../}} {{rb:to move the bird outside the room.}}"
    ]
    commands = [
        "mv bird ../",
        "mv bird .."
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def check_command(self):
        if self.last_user_input == "cat bird":
            # play cheep noise.
            self.send_hint("\nBird: {{Bb:Tweet!}}")
            return
        return StepTemplateChmod.check_command(self)

    def next(self):
        # alternatively, launch new window
        Animation("bird-animation").play_across_screen(speed=10)
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "The bird flew away",
        "",
        "Swordmaster: {{Bb:I found that bird when it was injured. It was time for it to be free.}}",
        "{{Bb:Come out and you will face your last challenge.}}"
    ]

    start_dir = "~/woods/clearing/house/cage-room"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cd ..",
        "cd ../"
    ]
    hints = [
        "Swordmaster: {{Bb:Use}} {{yb:cd ..}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep()

