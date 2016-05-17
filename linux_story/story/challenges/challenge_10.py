#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cd import TerminalCd
from linux_story.story.challenges.challenge_11 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 10


class Step1(StepTemplateCd):
    story = [
        _("You're in your house.  You appear to be alone."),
        _("Use {{lb:cat}} to {{lb:examine}} some of the objects around you.\n")
    ]
    allowed_commands = [
        "cat banana",
        "cat cake",
        "cat croissant",
        "cat grapes",
        "cat milk",
        "cat newspaper",
        "cat oven",
        "cat pie",
        "cat sandwich",
        "cat table"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    counter = 0
    deleted_items = ["~/my-house/kitchen/note"]
    story_dict = {
        "Eleanor, Edward, Edith, apple, dog": {
            "path": "~/town/.hidden-shelter",
        },
        "empty-bottle": {
            "path": "~/town/.hidden-shelter/basket"
        },
        "MV": {
            "path": "~/town/.hidden-shelter/.tiny-chest"
        }
    }
    # for check_command logic
    first_time = True

    def check_command(self):

        if self.last_user_input in self.allowed_commands:
            self.counter += 1
            self.allowed_commands.remove(self.last_user_input)
            hint = (
                _("\n{{gb:Well done!  Just look at one "
                  "more item.}}")
            )

        else:
            if self.first_time:
                hint = (
                    _("\n{{rb:Use}} {{lb:cat}} {{rb:to look at two of the "
                      "objects around you.}}")
                )
            else:
                hint = (
                    _("\n{{rb:Use the command}} {{yb:{}}} {{rb:to progress.}}") \
                        .format(self.allowed_commands[0])
                )

        level_up = (self.counter >= 2)

        if not level_up:
            self.send_text(hint)
            self.first_time = False
        else:
            return level_up

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        _("There doesn't seem to be anything here but loads of food."),
        _("See if you can find something back in {{bb:town}}."),
        _("First, use {{yb:cd ../}} to {{lb:leave}} the kitchen.\n")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/town"
    commands = [
        "cd ~/town",
        "cd ~/town/",
        "cd ..",
        "cd ../",
        "cd town",
        "cd town/",
        "cd ../..",
        "cd ../../",
        "cd"
    ]
    num_turns_in_home_dir = 0

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def show_hint(self):

        # decide command needed to get to next part of town
        if self.current_path == '~/my-house/kitchen' or \
                self.current_path == '~/my-house':

            # If the last command the user used was to get here
            # then congratulate them
            if self.last_user_input == "cd .." or \
                    self.last_user_input == 'cd ../':
                hint = (
                    _("\n{{gb:Good work!  Now replay the last command using "
                      "the UP arrow on your keyboard.}}")
                )

            # Otherwise, give them a hint
            else:
                hint = (
                    _("\n{{rb:Use}} {{yb:cd ../}} {{rb:to make your way to town.}}")
                )

        elif self.current_path == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = (
                    _("\n{{gb:Good work! Now use}} {{yb:cd town/}} {{gb: "
                      "to head to town.}}")
                )

            # Otherwise give them a hint
            else:
                hint = _("\n{{rb:Use}} {{yb:cd town/}} {{rb:to go into town.}}")

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_text(hint)

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        _("Use {{yb:ls}} to {{lb:look around}}.\n"),
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = _("{{rb:Use}} {{yb:ls}} {{rb:to have a look around the town.}}")

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        _("The place appears to be deserted."),
        _("However, you think you hear whispers."),
        # TODO make this writing small
        _("\n{{Bn:\".....if they use}} {{yb:ls -a}}{{Bn:, they'll see us...\"}}"),
        _("{{Bn:\"..Shhh!  ...might hear....\"}}\n")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls -a"
    hints = [
        _("{{rb:You heard whispers referring to}} {{yb:ls -a}}"
          "{{rb:, try using it!}}"),
    ]

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        _("You see a {{bb:.hidden-shelter}} that you didn't notice before."),
        _("{{gb:Something that starts with . is normally hidden from view.}}"),
        _("It sounds like the whispers are coming from there.  Try going in.\n")
    ]
    start_dir = "~/town"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cd .hidden-shelter",
        "cd .hidden-shelter/"
    ]
    hints = [
        _("{{rb:Try going inside the}} {{lb:.hidden-shelter}} {{rb:using }}"
          "{{lb:cd}}{{rb:.}}"),
        _("{{rb:Use the command}} {{yb:cd .hidden-shelter/ }}"
          "{{rb:to go inside.}}")
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        _("Is anyone there? Have a {{lb:look around}}.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to have a look around you.}}")
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
