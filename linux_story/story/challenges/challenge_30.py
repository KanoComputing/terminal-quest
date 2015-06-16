#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_31 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 30


class Step1(StepTemplateNano):
    story = [
        "{{pb:Ding. Dong.}}",
        "Eleanor: {{Bb:...what was that?}}",
        "Look around."
    ]
    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to check everyone is still present.}}"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Everyone seems to be here.",
        "What was that bell?",
        "Clara looks like she has something to say. {{lb:Listen to her.}}"
    ]
    commands = [
        "cat Clara"
    ]
    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"
    hints = [
        "{{rb:Use}} {{yb:cat Clara}} {{rb:to see what Clara has to say.}}"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Clara: {{Bb:Are you two going back out there?}}",
        "{{Bb:username, you look like you can take care of yourself, but "
        "I don't feel happy with Eleanor going outside.}}",
        "\nClara: {{Bb:username, will you leave Eleanor with me?}} "
        "{Bb:I'll look after her.}}",
        "{{\nyb:1: That's a good idea, take good care of her.}}",
        "{{yb:2: No I don't trust you, she's safer with me.}}",
        "{{yb:3: (Ask Eleanor.) Are you happy to stay here?}}",
        "{{yb:4: Do you have enough food here?}}",
        "\n{{lb:Reply to Clara.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"
    hints = [
        "{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:to reply "
        "to Clara.}}"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "echo 2":
            text = (
                "\nClara: {{Bb:Please let me look after her. "
                "I don't think it's safe for her to go outside.}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = "\nEleanor: {{Bb:I'm happy to stay here. I like Clara.}}"
            self.send_text(text)
        elif self.last_user_input == "echo 4":
            text = "\nClara: {{Bb:There's loads of food here, look in the}} "
            "{{lb:larder}} {{Bb:if you don't believe me.}}"
            self.send_text(text)
        else:
            StepTemplateNano.check_command(self, current_dir)

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "Clara: {{Bb:Thank you!}}",
        "Eleanor: {{Bb:When you find my parents, can you tell them I'm here?}}",
        "Clara: {{Bb:Where are you going to go now?}}",
        "\nLet's head back to see {{lb:Bernard}} and see if he's heard of this "
        "hermit. He seemed interested in this ability to lock doors.",
        "{{lb:Head to the shed-shop}}"
    ]
    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/shed-shop"
    commands = [
        "cd ../",
        "cd ..",
        "cd ../../",
        "cd ../..",
        "cd shed-shop/",
        "cd shed-shop",
        "cd ../../shed-shop",
        "cd ../../shed-shop/"
    ]

    def block_command(self, current_dir):
        return unblock_command_with_cd_hint(current_dir)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Look around"
    ]
    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"
    commands = [
        "ls",
        "ls -a"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
