#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.step_helper_functions import (
    unblock_commands_with_cd_hint
)
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
# import time
from linux_story.story.challenges.challenge_24 import Step1 as NextStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 23


class Step1(StepTemplateMkdir):
    story = [
        "You see Eleanor.  Listen to what she has to say."
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat Eleanor"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat Eleanor}} {{rb:to see what she has to say.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:\"Oh, it's you!",
        # "My parents went outside as we ran out of food."
        "Have you seen my Mum and Dad?\"}}",
        # TODO: change colour
        "\n{{yb:1: \"I'm afraid not.  When did you last see them?\"}}",
        "{{yb:2: \"Weren't they with you in the hidden-shelter?\"}}",
        "{{yb:3: \"(lie) Yes, I saw them in town.\"}}",
        "\n{{gb:Use the echo command to talk to Eleanor.}}"
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    def check_command(self, current_dir):
        if self.last_user_input in self.commands:
            return True
        elif self.last_user_input.startswith("echo"):
            text = (
                "\nEleanor: {{Bb:\"Pardon?  What did you say?\"}}"
            )
        else:
            text = (
                "\n{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} "
                "{{rb:or}} {{yb:echo 3}} {{rb:to reply.}}"
            )

        self.send_text(text)

    def next(self):
        Step3(self.last_user_input)


class Step3(StepTemplateMkdir):
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town"

    hints = [
        "{{rb:Use}} {{yb:cd ../}} {{rb:to go into town.}}"
    ]
    commands = [
        "cd ..",
        "cd ../",
        "cd ~/town",
        "cd ~/town/"
    ]

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.print_text = [
                "{{yb:\"I'm afraid not.  When did you last see them?\"}}\n"
            ]
            self.story += [
                "\nEleanor: {{Bb:\"Not long ago. The dog ran out again, "
                "so they went outside to look for him. "
                "I'm sure they're fine.\"}}"
            ]

        elif prev_command == "echo 2":
            self.print_text = [
                "{{yb:\"Weren't they with you in the hidden-shelter?\"}}\n"
            ]
            self.story += [
                "\nEleanor: {{Bb:No, they went outside. "
                "The dog ran away again, and then went outside to look for "
                "it. Maybe they got lost?\"}}"
            ]

        elif prev_command == "echo 3":
            self.print_text = [
                "{{yb:\"(lie) Yes, I saw them in town.\"}}\n"
            ]
            self.story += [
                "\nEleanor: {{Bb:\"Oh that's good! The bell scared me, but "
                "I'm pleased they're alright.\"}}"
            ]

        self.story += [
            "{{Bb:\"Let's go to town together and find them. I'm sure I'll be "
            "safe if I'm with you.\"}}",
            "\nEleanor joined you as a companion!",
            "{{lb:Leave the .hidden-shelter.}} "
            "Don't worry, Eleanor will follow!"
        ]

        StepTemplateMkdir.__init__(self)

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    start_dir = "~/town"
    end_dir = "~/town"
    hints = [
        "{{rb:Look around with}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    story = [
        "Eleanor: {{Bb:Let's go to the}} {{yb:east part}} "
        "{{Bb:of town.}}",
        "{{Bb:Have you not noticed it before? It's over there! "
        "Look over there.}}",
        "\nUse {{yb:ls}} to see what Eleanor is trying to show you."
    ]

    story_dict = {
        "Bernard": {
            "path": "~/town/east-part/shed-shop"
        },
        "best-shed-maker-in-the-world.sh, best-horn-in-the-world.sh": {
            "path": "~/town/east-part/shed-shop",
            "permissions": 0755
        },
        "NANO": {
            "path": "~/town/east-part/library/public-section"
        },
        "private-section": {
            "path": "~/town/east-part/library",
            # Remove all read and write permissions
            "permissions": 0000,
            "directory": True
        }
    }

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "You see a new part of town called {{lb:east-part}}.",
        "Eleanor: {{Bb:Lets go there and see if we can find my "
        "parents.}}",
        "\nGo into the east-part of town."
    ]
    start_dir = "~/town"
    end_dir = "~/town/east-part"

    hints = [
        "{{rb:Use}} {{lb:cd}} {{rb:to go into the "
        "east part of town}}",
        "{{rb:Use}} {{yb:cd east-part/}} {{rb:}}"
    ]
    last_step = True

    commands = [
        "cd east-part/",
        "cd east-part"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
