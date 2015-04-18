#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
from linux_story.Step import Step
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_20 import Step1 as NextChallengeStep


class StepTemplate(Step):
    challenge_number = 19

    def __init__(self, xp=""):
        Step.__init__(self, TerminalEcho, xp)


class Step1(StepTemplate):

    hints = [
        "{{rb:Use}} {{yb:echo}} {{rb:to reply to her "
        "question}}",
        "{{rb:Reply with yes by using}} {{gb:echo yes}}"
    ]

    commands = [
        "echo yes",
        "echo no",
        "echo Yes",
        "echo No",
        "echo YES",
        "echo NO"
    ]

    start_dir = "barn"
    end_dir = "barn"

    def __init__(self, xp=""):
        username = os.environ['LOGNAME']
        self.story = [
            "Ruth: {{Bb:Oh hello there!  You startled me.",
            "Do I know you?  You look familiar...",
            "Wait, you're Betty's kid aren't you!",
            "..."
            "Yes?  Do you have a tongue?",
            "Is your name not}} {{yb:" + username + "}}{{Bb:?}}",
            "\n{{gb:Reply with}} {{yb:echo yes}} "
            "{{gb:or}} {{yb:echo no}}."
        ]
        StepTemplate.__init__(self, xp)

    def check_command(self, line, current_dir):
        line = line.strip()
        self.answer = line
        return StepTemplate.check_command(self, line, current_dir)

    def next(self):
        Step2(self.answer)


class Step2(StepTemplate):
    start_dir = "barn"
    end_dir = "barn"
    commands = ["echo 1", "echo 2", "echo 3"]
    hints = [
        "{{rb:If you want to reply with \"Yes\", use}} {{yb:echo 1}}"
    ]

    def __init__(self, answer="echo yes"):

        if answer.lower() == "echo yes":
            self.story = [
                "Ruth: {{Bb:\"Ah, I knew it!\"}}"
            ]
        elif answer == "echo no":
            self.story = [
                "Ruth: {{Bb:\"Oh don't be ridiculous, you're the "
                "spitting image of Betty.\"}}"
            ]

        self.story = self.story + [
            "{{Bb:\"So you live in that little house outside town?}}",
            "{{yb:1: Yes}}",
            "{{yb:2: No}}",
            "{{yb:3: I don't know}}",
            "\n{{gb:Use}} {{yb:echo 1}}{{gb:,}} {{yb:echo 2}} {{gb:or}} "
            "{{yb:echo 3}} {{gb:to reply with either option 1, 2 or 3}}\n"
        ]

        StepTemplate.__init__(self)

    def check_command(self, line, current_dir):
        line = line.strip()
        if line in self.commands:
            # Record the command used so we can change the response
            self.command_used = line

        return StepTemplate.check_command(self, line, current_dir)

    def next(self):
        Step3(self.command_used)


# Option here to add a little exerpt where she mentions her dog was
# chasing a rabbit, and that we have to find the dog.
# We could go to the woods here, but not enter them.
class Step3(StepTemplate):
    start_dir = "barn"
    end_dir = "barn"

    # echo 3 should NOT pass this level
    commands = [
        "echo 1",
        "echo 2"
    ]
    hints = [
        "Ruth: {{Bb:\"Excuse me? What did you say? "
        "You know to use the}} {{yb:echo}} {{Bb:command, yes?\"}}",

        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}} {{rb:to reply}}"
    ]

    def __init__(self, prev_command='echo 1'):
        if prev_command == "echo 1":  # yes
            self.story = ["Ruth: {{Bb:\"I thought so!\"}}"]
        elif prev_command == "echo 2":  # no
            self.story = ["Ruth: {{Bb:Stop lying, I know you do.}}"]
        elif prev_command == "echo 3":  # I don't know
            self.story = ["Ruth: {{Bb:You don't know?  That's worrying...}}"]

        self.story = self.story + [
            "\n{{Bb:Did you walk all the way from Town? Did you see my husband there?",
            "He's a pretty}} {{yb:grumpy-man}}{{Bb:, he was travelling "
            "to town because of that big "
            "meeting with the Mayor}}",
            "\n{{yb:1: \"I'm sorry, he disappeared in front of me.\"}}",
            "{{yb:2: \"I didn't see your husband, but people have been "
            "disappearing in town\"}}",
            "{{yb:3: \"I don't know anything\"}}",
            "\nRespond to one of the following options using the {{yb:echo}} "
            "and option number."
        ]
        StepTemplate.__init__(self)

    def check_command(self, line, current_dir):
        line = line.strip()
        if line == "echo 1":  # Disappeared in front of me
            # go to next step
            return StepTemplate.check_command(self, line, current_dir)

        elif line == "echo 2":  # I didn't see him
            hint = (
                "Ruth: {{Bb:\"I feel like you're hiding something from "
                "me...\"}}"
            )
            self.send_hint(hint)
            return False

        elif line == "echo 3":  # I don't know anything
            hint = (
                "Ruth: {{Bb:Really?  Are you sure you didn't see a}} "
                "{{yb:grumpy-man}}{{Bb: in Town?}}"
            )
            self.send_hint(hint)
            return False

        self.send_hint()

        if len(self.hints) > 1:
            self.hints.pop(0)

        return False

    def next(self):
        Step4()


class Step4(StepTemplate):
    story = [
        "Ruth: {{Bb:\"He disappeared in front of you?? Oh no! "
        "They've been saying on the radio that people have been "
        "going missing...what should I do?\"}}",
        "\n{{yb:1: \"Some people survived by going into hiding.}}\"",
        "{{yb:2: \"I think you should go and look for your husband\"}}"
    ]

    start_dir = "barn"
    end_dir = "barn"

    commands = [
        "echo 1",
        "echo 2"
    ]

    hints = [
        "{{rb:Use}} {{yb:echo}} {{rb:plus an option number to "
        "respond to Ruth}}"
    ]

    def check_command(self, line, current_dir):
        line = line.strip()
        if line == "echo 1":  # Correct response
            # Can we asssume this is alright?
            return True
        elif line == "echo 2":
            response = (
                "Ruth: {{Bb:\"I would, but I'm scared of going missing myself."
                "...I know I'm a coward, he might come back, I should stay "
                "here in case he does.  Can you think of anything "
                "else?\"}}"
            )
            self.send_hint(response)

    def next(self):
        NextChallengeStep(self.xp)
