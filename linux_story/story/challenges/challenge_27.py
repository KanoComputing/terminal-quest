#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.challenges.challenge_28 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 27


class StepTemplateNano(TerminalNano):
    challenge_number = 27


class Step1(StepTemplateMkdir):
    story = [
        "You are back in the Bernard's place.",
        "{{lb:Listen to what Bernard has to say.}}"
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    hints = [
        "{{rb:Use}} {{yb:cat Bernard}} {{rb:to interact with Bernard.}}"
    ]

    commands = [
        "cat Bernard"
    ]

    deleted_items = ["~/town/east-part/library/Eleanor"]
    story_dict = {
        "Eleanor": {
            "path": "~/town/east-part/shed-shop"
        }
    }

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Bernard: {{Bb:Hellooooo. You came back to fix my script!}}",

        "Let's see whether we can fix it.",

        "Let's try and use {{yb:nano best-horn-in-the-world.sh}} to "
        "edit it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "nano best-horn-in-the-world.sh"
    ]

    hints = [
        "{{rb:Use}} {{yb:nano best-horn-in-the-world}} "
        "{{rb:to edit the tool.}}"
    ]

    nano_end_content = "echo \"Honk!\""
    goal_nano_filepath = "~/town/east-part/shed-shop/best-horn-in-the-world.sh"
    goal_nano_save_name = "best-horn-in-the-world.sh"

    # Overwrite the default behaviour for most of the steps - nano needs
    # slightly different behaviour.
    def check_command(self, current_dir):
        return self.check_nano_input()

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Now time to test your script!",
        "Use {{yb:./best-horn-in-the-world.sh}} to run it."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "./best-horn-in-the-world.sh"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    # Allow the user to ask all the questions within the same Step?
    story = [
        "{{gb:Congratulations, the script now prints \"Honk!\"}}",

        "\nBernard: {{Bb:The tool is working! Wonderful! "
        "Thank you so much!}}",

        "\nIt occurs to you that you haven't asked Bernard much about "
        "himself.",

        "What would you like to ask him?",

        "\n{{yb:1: \"What's the next big tool you want to create?\"}}",

        "{{yb:2: \"Are you going into hiding now?\"}}",

        "{{yb:3: \"What's in the secret room?\"}}",

        "\nUse {{lb:echo}} to ask him a question."
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part/shed-shop"

    commands = [
        "echo 1"
    ]

    def check_command(self, current_dir):
        if self.last_user_input == "echo 2":
            text = (
                "\nBernard: {{Bb:\"Er, what? No, I wasn't planning "
                "on doing so. Why would I do that?\"}}"
            )
            self.send_text(text)
        elif self.last_user_input == "echo 3":
            text = (
                "\nBernard: {{Bb:Oh ho ho ho, that's none of your business.}}"
            )
            self.send_text(text)
        else:
            return StepTemplateNano.check_command(self, current_dir)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:\"What's the next big tool you want to create?\"}}"
    ]

    story = [
        "Bernard: {{Bb:Well there are some spells I've heard "
        "about. Spells that lock doors, make items disappear, and "
        "even one that turns the user into a}} {{yb:superuser}}"
        "{{Bb:. Whatever that means.}}",

        "{{Bb:I guess the first I'd make is a key which locks "
        "doors, like in the}} {{lb:library}}.",

        "\nEleanor: {{Bb:I wonder how the librarian locked the }}"
        "{{lb:protected-section}} {{Bb:so people couldn't go in?}}",

        "{{Bb:Maybe she can give us information about where she found "
        "that?",

        "She might have gone into hiding somewhere. We should look "
        "for her.}}",

        "\n{{lb:Leave}} the shed-shop."
    ]

    commands = [
        "cd ..",
        "cd ../"
    ]

    start_dir = "~/town/east-part/shed-shop"
    end_dir = "~/town/east-part"
    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
