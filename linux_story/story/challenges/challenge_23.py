# challenge_23.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_eleanor import TerminalMkdirEleanor
from linux_story.story.challenges.challenge_24 import Step1 as NextStep


class StepMkdir(TerminalMkdir):
    challenge_number = 23


class StepMkdirEleanor(TerminalMkdirEleanor):
    challenge_number = 23


# ----------------------------------------------------------------------------------------


class Step1(StepMkdir):
    story = [
        _("You see {{bb:Eleanor}}. Listen to what she has to say.")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cat Eleanor"
    ]
    hints = [
        _("{{rb:Use}} {{yb:cat Eleanor}} {{rb:to see what she has to say.}}")
    ]

    def next(self):
        Step2()


class Step2(StepMkdir):
    story = [
        _("Eleanor: {{Bb:\"Oh, it's you! Have you seen my Mum and Dad?\"}}"),
        # TODO: change colour
        _("\n{{yb:1: \"I'm afraid not. When did you last see them?\"}}"),
        _("{{yb:2: \"Weren't they with you in the hidden-shelter?\"}}"),
        _("{{yb:3: \"(lie) Yes, I saw them in town.\"}}"),
        _("\nUse the {{yb:echo}} command to talk to {{bb:Eleanor}}.")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]

    def check_command(self):
        if self.last_user_input in self.commands:
            return True
        elif self.last_user_input.startswith("echo"):
            text = (
                _("\nEleanor: {{Bb:\"Pardon? What did you say?\"}}")
            )
        else:
            text = (
                _("\n{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} " +\
                "{{rb:or}} {{yb:echo 3}} {{rb:to reply.}}")
            )

        self.send_text(text)

    def next(self):
        Step3(self.last_user_input)


class Step3(StepMkdirEleanor):
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town"

    hints = [
        _("{{rb:Use}} {{yb:cd ..}} {{rb:to go into town.}}")
    ]

    eleanors_speech = (
        _("Eleanor: {{Bb:Yay, we're going on an adventure!}}")
    )

    def __init__(self, prev_command="echo 1"):
        self.story = []

        if prev_command == "echo 1":
            self.print_text = [
                _("{{yb:\"I'm afraid not. When did you last see them?\"}}")
            ]
            self.story += [
                _("Eleanor: {{Bb:\"Not long ago. The dog ran out again, " +\
                "so they went outside to look for him.\"}}")
            ]

        elif prev_command == "echo 2":
            self.print_text = [
                _("{{yb:\"Weren't they with you in the hidden-shelter?\"}}")
            ]
            self.story += [
                _("Eleanor: {{Bb:\"No, they went outside. " +\
                "The dog ran away again, so they went outside to look for " +\
                "it. Maybe they got lost?\"}}")
            ]

        elif prev_command == "echo 3":
            self.print_text = [
                _("{{yb:\"(lie) Yes, I saw them in town.\"}}")
            ]
            self.story += [
                _("Eleanor: {{Bb:\"Oh that's good! The dog ran away again, " +\
                "and they went outside to look for him.\""),
                _("\"The bell scared me, but I'm pleased they're alright.\"\n}}")
            ]

        self.story += [
            _("{{Bb:\"Let's go to town together and find them. I'm sure I'll be " +\
            "safe if I'm with you.\"}}"),

            _("\n{{gb:Eleanor joined you as a companion! You can check how " +\
            "she is any time with}} {{yb:cat Eleanor}}{{gb:.}}"),

            _("\n{{lb:Leave}} the {{bb:.hidden-shelter.}} " +\
            "Don't worry, {{bb:Eleanor}} will follow!")
        ]

        StepMkdirEleanor.__init__(self)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepMkdirEleanor):
    start_dir = "~/town"
    end_dir = "~/town"
    hints = [
        _("Eleanor: {{Bb:Have you forgotten how to look around? " +\
        "You need to use}} {{yb:ls}}{{Bb:.}}"),

        _("{{rb:Look around with}} {{yb:ls}}{{rb:.}}")
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/town/.hidden-shelter/Eleanor"]

    story = [
        _("Eleanor: {{Bb:\"Let's go to the}} {{bb:east}} " +\
        "{{Bb:of town.\"}}"),
        _("{{Bb:\"Haven't you noticed it before? It's over there! " +\
        "Look over there.\"}}"),
        _("\nUse {{yb:ls}} to see what {{bb:Eleanor}} is trying to show you.")
    ]

    story_dict = {
        "Bernard": {
            "path": "~/town/east/shed-shop"
        },
        "best-shed-maker-in-the-world.sh": {
            "path": "~/town/east/shed-shop",
            "permissions": 0755
        },
        "best-horn-in-the-world-incorrect.sh": {
            "name": "best-horn-in-the-world.sh",
            "path": "~/town/east/shed-shop",
            "permissions": 0755
        },
        "photocopier.sh, bernards-diary-1, bernards-diary-2": {
            "path": "~/town/east/shed-shop/basement"
        },
        "NANO": {
            "path": "~/town/east/library/public-section"
        },
        "private-section": {
            "path": "~/town/east/library",
            # Remove all read and write permissions
            "permissions": 0000,
            "directory": True
        },
        "Clara": {
            "path": "~/town/east/restaurant/.cellar"
        },
        "Eleanor": {
            "path": "~/town"
        }
    }

    eleanors_speech = (
        _("\nEleanor: {{Bb:Why are you looking at me? " +\
        "You should be looking over THERE.}}")
    )

    def next(self):
        Step5()


class Step5(StepMkdirEleanor):
    story = [
        _("You look in the direction {{bb:Eleanor}} is pointing."),
        _("There is a narrow road leading to another part of town."),
        _("This must take us to the {{bb:east}} part.\n"),
        _("Eleanor: {{Bb:Let's go there and see if we can find my " +\
        "parents.}}"),
        _("\n{{lb:Go}} into the {{bb:east}} of town.")
    ]
    start_dir = "~/town"
    end_dir = "~/town/east"

    hints = [
        _("{{rb:Use}} {{lb:cd}} {{rb:to go into the " +\
        "east part of town}}"),
        _("{{rb:Use}} {{yb:cd east}} {{rb:}}")
    ]
    last_step = True

    eleanors_speech = (
        _("\nEleanor: {{Bb:Let's go to the}} {{lb:east}} " +\
        "{{Bb:of town. Come on slow coach!}}")
    )

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
