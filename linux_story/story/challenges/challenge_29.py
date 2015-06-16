#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_30 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 29


class Step1(StepTemplateNano):
    story = [
        "Clara: {{Bb:What? Who are you?}}",

        "\nEleanor: {{Bb:Hello! I'm Eleanor, and this is}} {{gb:" +
        os.environ['LOGNAME'] + "}}{{Bb:.}}",
        "{{Bb:I recognise you!  You used to work in the library!}}",

        "\nClara: {{Bb:...ah, Eleanor! Yes, I remember you, you came in"
        " almost everyday.}}",

        # Options
        "\n{{yb:1: Why are you hiding down here?}}",
        "{{yb:2: How did you lock the protected-section?}}",
        "{{yb:3: Do you know about any other people in town?}}",

        "\nUse {{lb:echo}} to ask Clara a question."
    ]

    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"

    commands = [
        "echo 2"
    ]

    level_passed = False

    def check_command(self, current_dir):
        if self.last_user_input == "echo 1":
            # This apparently doesn't wrap around? :/
            text = [
                "\n{{yb:1: Why are you hiding down here?}}",
                "\nClara: {{Bb:I heard this bell go, and saw the "
                "lead librarian disappear in front of me. I was "
                "so scared I ran away, and found this .cellar here.}}",
            ]
            self.send_text(text)
        elif self.last_user_input == "echo 2":
            text = [
                "\n{{yb:2: How did you lock the protected-section}}",
                "\nClara: {{Bb:I didn't! The only person that could do that "
                "was lead librarian.",

                "He had to find a special command to be able to do that. "
                "I think he met a strange hermit outside town who taught him.",

                "I'm not sure where you'd find him, my best guess would be "
                "near the woods.",

                "\n{{gb:Press Enter to continue, or ask Clara more questions "
                "using}} {{lb:echo}}{{gb:.}}"
            ]
            self.send_text(text)
            self.level_passed = True
            # Add to the map?
        elif self.last_user_input == "echo 3":
            text = [
                "\n{{yb:2: Do you know about any other people in town?}}",
                "\nClara: {{Bb:There's a man I don't trust in the shed-shop. "
                "He makes very simple tools and charges a fortune for them.}}"
            ]
            self.send_text(text)
        # If no text is typed and the user entered "echo 2" on a previous
        # occasion, pass the level.
        elif not self.last_user_input and self.level_passed:
            return True

    def next(self):
        NextStep(self.xp)
