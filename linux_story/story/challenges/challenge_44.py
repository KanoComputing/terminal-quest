#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_rm import TerminalRm
from linux_story.story.challenges.challenge_45 import Step1 as NextStep


class StepTemplateRm(TerminalRm):
    challenge_number = 44


class Step1(StepTemplateRm):
    story = [
        "You destroyed the torn-note.",
        "The rm command gives you the power to {{lb:remove}} items.",
        "",
        "It is time to find that rabbit.",
        "Go to where you met the rabbit."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/thicket"

    hints = [
        "Remember where you met the rabbit?",
        "You met the rabbit in the woods",
        "Go to ~/woods/thicket"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateRm):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    hint = [
        "Use ls to look around"
    ]

    def next(self):
        Step3()


# Outside the rabbithole.
class Step3(StepTemplateRm):
    story = [
        "You are outside the rabbithole. Try and go inside."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]
    # story_dict = {
    #     "rabbithole": {
    #         "path": "~/woods/thicket",
    #         "permissions": 0000
    #     }
    # }
    file_list = [
        {
            "type": "directory",
            "path": "~/woods/thicket/rabbithole",
            "permissions": 0000
        }
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplateRm):
    story = [
        "It looks like it is locked to us. The rabbit must have learnt how to lock the directory",
        "Unlock it."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"

    commands = [
        # wrap this in a function?
        "chmod +rwx rabbithole",
        "chmod +rwx rabbithole/",
        "chmod +rxw rabbithole",
        "chmod +rxw rabbithole/",
        "chmod +wxr rabbithole",
        "chmod +wxr rabbithole/",
        "chmod +wrx rabbithole",
        "chmod +wrx rabbithole/",
        "chmod +xwr rabbithole",
        "chmod +xwr rabbithole/",
        "chmod +xrw rabbithole",
        "chmod +xrw rabbithole/"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateRm):
    story = [
        "Now go inside"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]

    # story_dict = {
    #     "bell, Rabbit": {
    #         "path": "~/woods/thicket/rabbithole"
    #     },
    #     # these should be moved as in appropriate in the story
    #     "Mum, Dad, dog, Edith, Edward, grumpy-man, Mayor, young-girl, little-boy": {
    #         "path": "~/woods/thicket/rabbithole/cage"
    #     }
    # }
    file_list = [
        {
            "path": "~/woods/thicket/rabbithole/bell",
            "type": "file",
            "contents": get_story_file("bell"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/Rabbit",
            "type": "file",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mum",
            "type": "file",
            "contents": get_story_file("Mum"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Dad",
            "type": "file",
            "contents": get_story_file("Dad"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/dog",
            "type": "file",
            "contents": get_story_file("dog"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edith",
            "type": "file",
            "contents": get_story_file("Edith"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edward",
            "type": "file",
            "contents": get_story_file("Edward"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/grumpy-man",
            "type": "file",
            "contents": get_story_file("grumpy-man"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mayor",
            "type": "file",
            "contents": get_story_file("Mayor"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/young-girl",
            "type": "file",
            "contents": get_story_file("young-girl"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/little-boy",
            "type": "file",
            "contents": get_story_file("little-boy"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/swordmaster",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0644
        }
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep()