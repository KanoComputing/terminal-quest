#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os

# At this point, Bernard disappears, so no need to keep blocking access to
# his basement.
from linux_story.story.terminals.terminal_eleanor import TerminalNanoEleanor
from linux_story.story.challenges.challenge_31 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepNano(TerminalNanoEleanor):
    challenge_number = 30


class Step1(StepNano):
    story = [
        "{{pb:Ding. Dong.}}",
        "\nEleanor: {{Bb:...what was that?}}",
        "{{lb:Look around.}}"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to check everyone is still present.}}"
    ]
    deleted_items = [
        "~/town/east/shed-shop/Bernard"
    ]
    story_dict = {
        "bernards-hat": {
            "path": "~/town/east/shed-shop"
        }
    }
    eleanors_speech = (
        "Eleanor: {{Bb:......}}"
    )

    def next(self):
        Step2()


class Step2(StepNano):
    story = [
        "Everyone seems to be here. What was that bell?",
        "\nClara looks like she has something to say. {{lb:Listen to her.}}"
    ]
    commands = [
        "cat Clara"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    hints = [
        "{{rb:Use}} {{yb:cat Clara}} {{rb:to see what Clara has to say.}}"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:....I was so scared. I don't think I want to go "
        "outside now.}}"
    )

    def next(self):
        Step3()


class Step3(StepNano):
    story = [
        "Clara: {{Bb:Are you two going back out there?}}",
        "{{gb:" + os.environ['LOGNAME'] + "}}"
        "{{Bb:, you look like you can take care of yourself, but "
        "I don't feel happy with Eleanor going outside.}}",
        "\n" + "{{gb:" + os.environ['LOGNAME'] + "}}"
        "{{Bb:, will you leave Eleanor with me? "
        "I'll look after her.}}",
        "\n{{yb:1: That's a good idea, take good care of her.}}",
        "{{yb:2: No I don't trust you, she's safer with me.}}",
        "{{yb:3: (Ask Eleanor.) Are you happy to stay here?}}",
        # "{{yb:4: Do you have enough food here?}}",
        "\n{{lb:Reply to Clara.}}"
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/restaurant/.cellar"
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}} {{rb:to reply to Clara.}}"
    ]
    eleanors_speech = (
        "Eleanor: {{Bb:I'm happy to stay here. I like Clara.}}"
    )

    def check_command(self):
        if self.last_user_input == "echo 2":
            text = (
                "\nClara: {{Bb:Please let me look after her. "
                "I don't think it's safe for her to go outside.}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = "\nEleanor: {{Bb:I'm happy to stay here. I like Clara.}}"
            self.send_text(text)
        # elif self.last_user_input == "echo 4":
        #    text = (
        #        "\nClara: {{Bb:There's loads of food here, look in the}} "
        #        "{{lb:larder}} {{Bb:if you don't believe me.}}"
        #    )
        #    self.send_text(text)
        else:
            return StepNano.check_command(self)

    def next(self):
        Step4()


class Step4(StepNano):
    story = [
        "Clara: {{Bb:Thank you!}}",
        "Eleanor: {{Bb:When you find my parents, can you tell them I'm "
        "here?}}",
        "Clara: {{Bb:Where are you going to go now?}}",
        "\nLet's head back to see {{lb:Bernard}} and see if he's heard of "
        "the {{lb:masked swordsmaster}}.",
        "{{lb:Head to the shed-shop.}}"
    ]
    start_dir = "~/town/east/restaurant/.cellar"
    end_dir = "~/town/east/shed-shop"
    last_step = True

    path_hints = {
        "~/town/east/restaurant/.cellar": {
            "blocked": "\n{{rb:Use}} {{yb:cd ../}} {{rb:to go back.}}"
        },
        "~/town/east/restaurant": {
            "not_blocked": "\n{{gb:Good work! Keep going!}}",
            "blocked": "\n{{rb:Use}} {{yb:cd ../}} {{rb:to go back.}}"
        },
        "~/town/east": {
            "not_blocked": "\n{{gb:Now go into the}} {{lb:shed-shop}}{{gb:.}}",
            "blocked": "\n{{rb:Use}} {{yb:cd shed-shop/}}{{rb:.}}"
        }
    }

    def check_command(self):
        if self.current_path == self.end_dir:
            return True
        elif "cd" in self.last_user_input and not self.get_command_blocked():
            hint = self.path_hints[self.current_path]["not_blocked"]
        else:
            hint = self.path_hints[self.current_path]["blocked"]

        self.send_text(hint)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        NextStep(self.xp)
