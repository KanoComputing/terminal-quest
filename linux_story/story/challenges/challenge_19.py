# challenge_18.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_20 import Step1 as NextStep


class StepTemplateEcho(TerminalEcho):
    challenge_number = 19


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    username = os.environ['LOGNAME']
    story = [
        _("Ruth: {{Bb:\"You startled me!\""),
        _("\"Do I know you? You look familiar...\""),
        _("\"Wait, you're}} {{bb:Mum}}{{Bb:'s kid, aren't you!\""),
        _("\"...Yes? Do you have a tongue?\""),
        _("\"Is your name not}} {{yb:{}}}{{Bb:?\"}}").format(username),
        _("\n{{gb:Reply with}} {{yb:echo yes}} {{gb:or}} {{yb:echo no}}.")
    ]

    # Story has been moved to
    hints = [
        _("{{rb:Use}} {{yb:echo}} {{rb:to reply to her question.}}"),
        _("{{rb:Reply with yes by using}} {{yb:echo yes}}{{rb:.}}")
    ]

    commands = [
        "echo yes",
        "echo Yes",
        "echo YES"
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    def check_command(self):

        if self.last_user_input == "echo no" or \
                self.last_user_input == "echo No" or \
                self.last_user_input == "echo NO":
            hint = (
                _("Ruth: {{Bb:\"Oh don't be ridiculous, you look just like her.\"}}")
            )
            self.send_hint(hint)

        return StepTemplateEcho.check_command(self)

    def next(self):
        Step2()


class Step2(StepTemplateEcho):
    print_text = [_("{{yb:\"Yes\"}}")]

    story = [
        _("Ruth: {{Bb:\"Ah, I knew it!\"}}"),
        _("{{Bb:\"So you live in that little house outside town?\"}}"),
        # TODO: see if this can appear as a block
        # TODO: change the colour of this.
        _("{{yb:1: \"Yes\"}}"),
        _("{{yb:2: \"No\"}}"),
        _("{{yb:3: \"I don't know\"}}"),
        _("\n{{gb:Use}} {{yb:echo 1}}{{gb:,}} {{yb:echo 2}} {{gb:or}} {{yb:echo 3}} {{gb:to reply with either option 1, 2 or 3.}}\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    commands = ["echo 1", "echo 2", "echo 3"]
    hints = [
        _("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} {{yb:echo 3}} {{rb:to reply to Ruth.}}")
    ]

    def check_command(self):
        replies = {
            "echo yes": "1",
            "echo no": "2",
            "echo \"i don't know\"": "3",
            "echo i don't know": "3"
        }

        if self.last_user_input.lower() in replies:
            hint = [
                _("\n{{rb:If you want to reply with \"{}\", use}} {{yb:echo {}}}") \
                        .format(self.last_user_input, replies[self.last_user_input.lower()])
            ]
            self.send_text(hint)
        else:
            return StepTemplateEcho.check_command(self)

    def next(self):
        Step3(self.last_user_input)


# Option here to add a little exerpt where she mentions her dog was
# chasing a rabbit, and that we have to find the dog.
# We could go to the woods here, but not enter them.
class Step3(StepTemplateEcho):
    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"

    # echo 3 should NOT pass this level
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        _("Ruth: {{Bb:\"Excuse me? What did you say? You know to use the}} {{lb:echo}} {{Bb:command, yes?\"}}"),
        _("{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} {{yb:echo 3}} {{rb:to reply.}}")
    ]

    def __init__(self, prev_command='echo 1'):
        if prev_command == "echo 1":  # yes
            self.print_text = [_("{{yb:\"Yes\"}}")]
            self.story = [_("Ruth: {{Bb:\"I thought so!\"}}")]
        elif prev_command == "echo 2":  # no
            self.print_text = [_("{{yb:\"No\"}}")]
            self.story = [_("Ruth: {{Bb:\"Stop lying, I know you do.\"}}")]
        elif prev_command == "echo 3":  # I don't know
            self.print_text = [_("{{yb:\"I don't know\"}}")]
            self.story = [_("Ruth: {{Bb:\"You don't know? That's worrying...\"}}")]

        self.story = self.story + [
            _("\n{{Bb:\"Did you walk all the way from town? Did you see my husband there?"),
            _("He's a pretty}} {{bb:grumpy-man}}{{Bb:, he was travelling to town because of that big meeting with the Mayor.\"}}"),
            _("\n{{yb:1: \"I'm sorry, he disappeared in front of me.\"}}"),
            _("{{yb:2: \"I didn't see your husband, but people have been disappearing in town.\"}}"),
            _("{{yb:3: \"I don't know anything.\"}}"),
            _("\nRespond with one of the following options using the {{yb:echo}} command and option number.\n")
        ]
        StepTemplateEcho.__init__(self)

    def check_command(self):
        if self.last_user_input == "echo 1":  # Disappeared in front of me
            # go to next step
            return StepTemplateEcho.check_command(self)

        elif self.last_user_input == "echo 2":  # I didn't see him
            hint = (
                _("Ruth: {{Bb:\"I feel like you're hiding something from me...\"}}")
            )
            self.send_hint(hint)
            return False

        elif self.last_user_input == "echo 3":  # I don't know anything
            hint = (
                _("Ruth: {{Bb:\"Really? Are you sure you didn't see a}} {{lb:grumpy-man}}{{Bb: in town?\"}}")
            )
            self.send_hint(hint)
            return False

        else:
            # Show default hint
            self.send_hint()
            return False

    def next(self):
        Step4()


class Step4(StepTemplateEcho):
    print_text = [
        _("{{yb:\"I'm sorry, he disappeared in front of me.\"}}")
    ]
    story = [
        _("Ruth: {{Bb:\"He disappeared in front of you?? Oh no! They've been saying on the radio that people have been going missing...what should I do?\"}}"),
        _("\n{{yb:1: \"Some people survived by going into hiding.\"}}"),
        _("{{yb:2: \"I think you should go and look for your husband\"}}\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/barn"
    last_step = True

    commands = [
        "echo 1",
        "echo 2"
    ]

    hints = [
        _("Ruth: {{Bb:What did you say? I didn't catch that.}}"),
        _("{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:to reply.}}")
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":  # Correct response
            # Can we assume this is alright?
            return True
        elif self.last_user_input == "echo 2":
            response = (
                _("Ruth: {{Bb:\"I would, but I'm scared of going missing myself.\"\n\"He might come back, so I should stay here in case he does. Can you think of anything else?\"}}")
            )
            self.send_hint(response)
        else:
            self.send_hint()

    def next(self):
        NextStep(self.xp)
