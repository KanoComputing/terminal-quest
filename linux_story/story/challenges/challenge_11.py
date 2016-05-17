# challenge_11.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_cd import TerminalCd

# Change this import statement, need to decide how to group the terminals
# together
from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.challenges.challenge_12 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_commands
from linux_story.common import tq_file_system


class StepTemplateCd(TerminalCd):
    challenge_number = 11


class StepTemplateMv(TerminalMv):
    challenge_number = 11


# ----------------------------------------------------------------------------------------


# The next few steps should be like the disappearing of people in the town
class Step1(StepTemplateCd):
    story = [
        _("You see a group of scared looking people and a {{bb:dog}}.\n"),
        _("{{lb:Listen}} to what they have to say with {{yb:cat}}.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"

    # Use functions here
    all_commands = {
        "cat Edith": _("\n{{wb:Edith:}} {{Bb:\"You found us! Edward, I told "
        "you to keep your voice down.\"}}"),
        "cat Eleanor": _("\n{{wb:Eleanor:}} {{Bb:\"My mummy is scared the "
        "bell will find us if we go outside.\"}}"),
        "cat Edward": _("\n{{wb:Edward:}} {{Bb:\"I'm sorry Edith...but "
        "I don't think they mean any harm. Maybe they could help us?\"}}"),
        "cat dog": _("\n{{wb:Dog:}} {{Bb:\"Woof woof!\"}}")
    }

    def check_command(self):

        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls':
            hint = _("\n{{gb:You look around.}}")
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
            _("{{rb:Use}} {{yb:{}}} {{rb:to progress.}}") \
               .format(self.all_commands.keys()[0])
        ]

        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands.keys() and \
                end_dir_validated:
            # Print hint from person
            hint = "\n" + self.all_commands[self.last_user_input]

            self.all_commands.pop(self.last_user_input, None)

            if len(self.all_commands) > 0:
                hint += _("\n{{gb:Well done! Check on {} more.}}\n") \
                    .format(str(len(self.all_commands)))
            else:
                hint += _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Don't pass unless the user has emptied self.all_commands
        return False

    def next(self):
        Step2()


# After we've heard some of the story from all the people
class Step2(StepTemplateMv):
    story = [
        _("Edward looks like he has something he wants to say to you.\n"),
        _("{{wb:Edward:}} {{Bb:\"Hi there. Can you help me with something?\""),

        _("\"I learnt this spell for moving items from"
          " one place to another. But I can't seem to make it work.\""),

        _("\"I've been trying to move this}} {{bb:apple}} {{Bb:into the}} "
          "{{bb:basket}}{{Bb:\"}}"),

        _("{{Bb:\"I was told the command was}} {{yb:mv apple basket/}}{{Bb:\"}}"),

        _("{{Bb:\"But I don't understand what that means. Do I say it? "
          "Or write it?\"}}\n"),

        _(" ------------------------------------- "),
        _("| {{gb:New Spell}}: to {{lb:move}} objects, type {{yb:mv}} |"),
        _("| and the object name.                |"),
        _(" ------------------------------------- ")
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv apple basket",
        "mv apple basket/"
    ]
    highlighted_commands = ['mv']
    hints = [
        _("{{rb:Use the command}} {{yb:mv apple basket/}} {{rb:to "
          "move the apple into the basket.}}")
    ]
    # This is to add the apple into the virtual tree
    # we would like to integrate when using mv with the tree
    # automatically

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step3()


class Step3(StepTemplateMv):
    story = [
        _("Check you've managed to move the {{bb:apple}}. {{lb:Look around}} "
          "in this directory.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    story_dict = {
        "apple": {
            "path": "~/town/.hidden-shelter/basket"
        }
    }

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        _("{{gb:Nice work! The apple isn't in this directory anymore.}}\n"),
        _("{{wn:Now check the apple is in the}} {{bb:basket}} {{wn:using}} "
          "{{yb:ls}}{{wn:.}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls basket",
        "ls basket/",
        "ls -a basket",
        "ls -a basket/"
    ]
    hints = [
        _("{{rb:Use the command}} {{yb:ls basket/}} {{rb:to look in the "
          "basket.}}")
    ]

    def next(self):
        Step5()


# After cat-ing the person again?
class Step5(StepTemplateMv):
    story = [
        _("{{gb:Excellent, you moved the apple into the basket!}}"),
        _("\n{{wb:Edward:}} {{Bb:\"Hey, you did it! What was I doing "
          "wrong?\"}}"),
        _("{{Bb:\"Can you move the apple from the basket back here?\"}}\n"),
        _("{{lb:Move}} the {{bb:apple}} from the {{bb:basket}} "
          "to your current position. This is represented by {{bb:./}} \n"),
        _("So {{yb:mv basket/apple ./}} is the full command. "
          "You need the {{bb:./}} !\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv basket/apple .",
        "mv basket/apple ./"
    ]
    hints = [
        _("{{rb:Use the command}} {{yb:mv basket/apple ./}} {{rb:to move "
          "the apple from the basket to your current position}} {{bb:./}}")
    ]

    def block_command(self):
        if self.last_user_input == "mv basket/apple":
            hint = (
                _("{{gb:Nearly! The full command is}} "
                  "{{yb:mv basket/apple ./}} {{gb:- don't forget the dot!}}")
            )
            self.send_hint(hint)
            return True
        else:
            return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        Step6()


class Step6(StepTemplateMv):
    story = [
        _("{{wb:Edith:}} {{Bb:\"You should stop playing with that, that's the "
          "last of our food.\"}}"),
        _("{{Bb:\"Ah! The dog ran outside!\"}}"),
        _("{{wb:Eleanor:}} {{Bb:\"Doggy!\"}}"),
        _("{{wb:Edith:}} {{Bb:\"No, honey! Don't go outside!\"}}"),
        _("\n{{bb:Eleanor}} follows her {{bb:dog}} and leaves the "
          "{{bb:.hidden-shelter}}."),
        _("{{lb:Look around}} to check this.\n")
    ]
    story_dict = {
        "Eleanor": {
            "path": "~/town"
        },
        "dog": {
            "path": "~/town"
        }
    }
    deleted_items = [
        '~/town/.hidden-shelter/Eleanor',
        '~/town/.hidden-shelter/dog'
    ]

    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls", "ls -a"
    ]
    hints = [
        _("{{rb:Look around using}} {{yb:ls}} {{rb:to check if Eleanor is "
          "here.}}")
    ]

    def next(self):
        Step7()


class Step7(StepTemplateMv):
    story = [
        _("{{wb:Edith:}} {{Bb:\"No!! Honey, come back!!\"}}"),
        _("{{Bb:\"You there, save my little girl!\"}}\n"),
        _("First, {{lb:look outside}} for {{bb:Eleanor}} with {{yb:ls ../}}"),
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = ""
    commands = [
        "ls ..",
        "ls ../",
        "ls ~/town",
        "ls ~/town/"
    ]
    hints = [
        _("{{rb:Look in the town directory by using either}} {{yb:ls ../}} "
          "{{rb:or}} {{yb:ls ~/town/}}")
    ]

    def next(self):
        Step8()


class Step8(StepTemplateMv):
    story = [
        _("Now {{lb:move}} {{bb:Eleanor}} from the {{bb:town}} outside {{bb:..}} to "
          "your current position {{bb:.}}\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "mv ../Eleanor .",
        "mv ../Eleanor ./",
        "mv ~/town/Eleanor ~/town/.hidden-shelter",
        "mv ~/town/Eleanor ~/town/.hidden-shelter/",
        "mv ~/town/Eleanor .",
        "mv ~/town/Eleanor ./",
        "mv ../Eleanor ~/town/.hidden-shelter",
        "mv ../Eleanor ~/town/.hidden-shelter/",
    ]
    hints = [
        _("{{rb:Quick! Use}} {{yb:mv ../Eleanor ./}} "
          "{{rb:to move the little girl back to safety.}}")
    ]
    last_step = True
    girl_file = os.path.join(tq_file_system, 'town/.hidden-shelter/Eleanor')

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def check_command(self):

        if os.path.exists(self.girl_file):
            return True

        else:
            self.send_hint()
            return False

    def next(self):
        NextStep(self.xp)
