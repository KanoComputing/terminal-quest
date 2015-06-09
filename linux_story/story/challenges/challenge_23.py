#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story


# from linux_story.step_helper_functions import (
#    unblock_commands
# )
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
# import time
# from linux_story.story.challenges.challenge_24 import Step1 as NextChallengeStep


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
        "Eleanor: {{Bb:Oh, it's you! Thank you for finding me!",
        # "My parents went outside as we ran out of food."
        "I heard this bell. Do you know where my Mum and Dad are?}}",
        "\n{{gb:Use the echo command to talk to Eleanor.}}",
        # TODO: change colour
        "{{yb:1: \"Weren't they with you in the hidden-shelter?\"}}"
        "{{yb:2: \"Did you see anything strange?\"}}"
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        "{{rb:NO HINTS}}"
    ]

    def next(self):
        Step3(self.last_user_input)


class Step3(StepTemplateMkdir):
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]
    hints = [
        "{{rb:NO HINTS}}"
    ]

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.story += [
                "{{yb:\"Weren't they with you in the hidden-shelter?\"}}",
                "Eleanor: {{Bb:No, the dog ate all the food, so they went to find some more.",
                "Then I heard the bell",
                "I guess they disappeared?}}"
            ]

        elif prev_command == "echo 2":
            self.story += [
                "{{yb:\"Did you see anything strange?\"}}",
                "Eleanor: {{Bb:No, I didn't see anything.}}",
                "{{Bb:My parents were outside the shelter looking for food, so I was by myself.}}",
                "{{Bb:Do you think they disappeared?}}"
            ]

        self.story = [
            "{{gb:Use echo to reply.}}",
            "{{yb:1: \"Yes, I saw people disappear in \"}}",
            "{{yb:2: \"(lie) No, I saw them outside.\"}}",
            "{{yb:3: \"Probably. My Mum and Dad also disappeared.\"}}"
        ]

        StepTemplateMkdir.__init__(self)

    def next(self):
        Step4(self.command_used)


class Step4(StepTemplateMkdir):
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town"

    hints = [
        "{{rb:NO HINTS}}"
    ]

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.story += [
                "{{yb:1: \"Yes\"}}",
                "Eleanor: {{Bb:No, they went to get food.}}"
            ]

        elif prev_command == "echo 2":
            self.story += [
                "{{yb:\"(lie) No\"}}",
                "Eleanor: {{Bb:I don't believe you.}}"
            ]

        elif prev_command == "echo 3":
            self.story += [
                "{{yb:\"My Mum and Dad also disappeared.\"}}",
                "Eleanor: {{Bb:Let's find them!}}"
            ]

        self.story += [
            "{{Bb:Maybe there are other people like us in town.}}",
            "{{Bb:Let's look! I can show you around.}}",
            "{{gb:Let's go back to town. Use}} {{yb:cd}} {{gb:to head back.}}"
        ]

        StepTemplateMkdir.__init__(self)

    def next(self):
        Step5(self.command_used)


class Step5(StepTemplateMkdir):
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"

    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    hints = [
        "{{rb:NO HINTS}}"
    ]

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.story += [
                "{{yb:You said: \"Weren't they with you in the "
                "hidden-shelter?\"}}",
                "Eleanor: No."
            ]

        elif prev_command == "echo 2":
            self.story += [
                "{{yb:You said: \"Did you see your parents disappear?\"}}",
                "Eleanor: No."
            ]

        elif prev_command == "echo 3":
            self.story += [
                "{{yb:You said: \"My Mum and Dad also disappeared.\"}}",
                "Eleanor: No."
            ]

        StepTemplateMkdir.__init__(self)
