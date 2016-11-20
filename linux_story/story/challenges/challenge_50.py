#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
import os

from linux_story.Animation import Animation
from linux_story.story.terminals.terminal_sudo import TerminalSudo


class StepTemplateSudo(TerminalSudo):
    challenge_number = 50


class Step1(StepTemplateSudo):
    story = [
        "You are outside the rabbithole. Look more closely at the rabbithole, and then try and go inside."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]
    story_dict = {
        "rabbithole": {
            "path": "~/woods/thicket",
            "permissions": 0700,
            "owner": "rabbit"
        }
    }


    def next(self):
        Animation("firework-animation").play_finite(cycles=1)
        Step2()


class Step2(StepTemplateSudo):
    story = [
        "It looks like the rabbit owns the rabbithole, and has removed the write permissions for us.",
        "",
        "Use sudo to go into the rabbithole"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "sudo cd rabbithole",
        "sudo cd rabbithole/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateSudo):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "sudo ls",
        "sudo ls .",
        "sudo ls ./"
    ]

    def check_command(self):
        if self.last_user_input == "ls":
            self.send_hint("You need to use {{yb:sudo ls}} to look around.")
            return
        return StepTemplateSudo.check_command(self)

    def next(self):
        Step4()


class Step4(StepTemplateSudo):
    story = [
        "Go into the extra directory you see in front of you."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole/dir"

    commands = [
        "sudo cd dir",
        "sudo cd dir/"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateSudo):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket/rabbithole/dir"
    end_dir = "~/woods/thicket/rabbithole/dir"

    commands = [
        "sudo ls",
        "sudo ls .",
        "sudo ls ./"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateSudo):
    story = [
        "You see the rabbit in front of you, and a cage. Investigate."
    ]
    start_dir = "~/woods/thicket/rabbithole/dir"
    end_dir = "~/woods/thicket/rabbithole/dir"

    commands = [
        "sudo cat rabbit",
        "sudo ls cage"
    ]

    # make all the people respond appropriately when cat is used on them.

    def next(self):
        Step7()


class Step7(StepTemplateSudo):
    # change rabbit ascii for this?
    story = [
        "Rabbit: {{Bb:...}}",
        "The rabbit looks frustrated.",
        "There is a hutch in the directory...maybe you can lock him up"
        "You should try and lock him up!"
    ]
    start_dir = "~/woods/thicket/rabbithole/dir"
    end_dir = "~/woods/thicket/rabbithole/dir"

    def check_command(self):
        hutch_path = os.path.join(self.real_path, "hutch")
        rabbit_path = os.path.join(hutch_path, "rabbit")
        if os.access(hutch_path, os.W_OK) and os.path.exists(rabbit_path):
            return True

    # make all the people respond appropriately when cat is used on them.

    def next(self):
        Animation("firework-animation").play()
        self.send_hint("Done!")
