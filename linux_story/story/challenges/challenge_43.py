#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import time

from linux_story.common import get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.terminals.terminal_rm import TerminalRm
from linux_story.story.challenges.challenge_44 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 43


class StepTemplateRm(TerminalRm):
    challenge_number = 43


REPLY_PRINT_TEXT = ["A rabbit came and stole the command in front of us."]
SWORDMASTER_STORY = [
        "Swordmaster: {{Bb:I see.}}",
        "{{Bb:You idiot. Did you bring the rabbit with you?}}",
        "{{Bb:I met a white rabbit before, but It was an innocent creature then.}}",
        "{{Bb:Perhaps he is}} {{lb:possessed}}{{Bb.}}",
        "{{Bb:We must remove the source of the problem. I will teach you how to.}}"
]


class Step1(StepTemplateChmod):
    story = [
        "You are standing alone in the library. The rabbit has stolen the command, and you have an increased sense of "
        "impending doom.",
        "The swordmaster runs into the room.",
        "Swordmaster: {{Bb:What have you done?}}",
        "",
        "{{yb:1: A rabbit came and stole the command in front of us.}}",
        "{{yb:2: Nothing.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    file_list = [
        {
            "path": "~/town/east/library/private-section/swordmaster",
            "contents": get_story_file("swordmaster"),
            "permissions": 0644,
            "type": "file"
        }
    ]
    commands = [
        "echo 1",
        "echo 2"
    ]
    user_replies = {
        "echo 1:": "A rabbit came and stole the command in front of us.",
        "echo 2": "Nothing."
    }
    extra_hints = {
        "echo 2": "Swordmaster: {{Bb:Tell me the truth.}}"
    }
    hints = [
        "Swordmaster: {{Bb:Speak with}} {{lb:echo}} {{Bb:and tell me!}}"
    ]

    def next(self):
        if self.last_user_input == "echo 1":
            Step21()
        else:
            StepAngrySwordMaster(user_reply=self.user_replies[self.last_user_input])


class StepAngrySwordMaster(StepTemplateChmod):
    story = [
        "Swordmaster: {{rb:ENOUGH!}}",
        "{{Bb:Tell me}} {{rb:the truth}}",
        "{{Bb:You need my help to fix this....}}",
        "{{yb:1: A rabbit came and stole the command in front of us.}}",
        "{{yb:2: Nothing.}}"
    ]
    commands = [
        "echo 1",
        "echo 2"

    ]
    user_replies = {
        "echo 1:": "A rabbit came and stole the command in front of us.}}",
        "echo 2": "Nothing."
    }
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def __init__(self, user_reply):
        self.print_text = [user_reply]
        StepTemplateChmod.__init__(self)

    def next(self):
        if self.last_user_input == "echo 1":
            Step2()
        else:
            GameOver()


class GameOver(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:You stole it, didn't you?",
        "Then it's time to end this.}}"
    ]

    def next(self):
        self.send_hint("Game over!")
        time.sleep(3)
        self.exit()


class Step11(StepTemplateChmod):
    print_text = REPLY_PRINT_TEXT
    story = SWORDMASTER_STORY + [
        "{{Bb:Do you know why they call me the swordmaster? Because I know the art of removing.}}",
        "{{Bb:Meet me back at my house.}}",
        "",
        "The swordmaster leaves the library."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/clearing/house"
    hints = [
        "Follow the swordmaster. Go back to his house."
    ]
    counter = 0

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def check_command(self):
        end_dir_validated = self._validate_end_dir()
        if self.counter >= 3:
            if not end_dir_validated:
                self.send_hint()
        else:
            self.counter += 1

        return self._client.finish_if_server_ready(end_dir_validated)

    def next(self):
        Step12()


class Step12(StepTemplateChmod):
    story = [
        "Listen to the swordmaster."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cat swordmaster"
    ]
    hints = [
        "Talk to him with {{yb:cat swordmaster}}"
    ]

    def next(self):
        Step13()


class Step13(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:During my time as a librarian, I found an ancient sword with the power to destroy.}}",
        "{{Bb:Take my sword and examine it closely.}}",
        "",
        "The swordmaster gave you his sword! {{lb:Examine}} the sword."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cat sword"
    ]

    deleted_items = [
        "~/woods/clearing/house/swordmaster"
    ]

    file_list = [
        {
            "path": "~/woods/clearing/house/swordmaster",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0755
        },
        {
            "path": "~/woods/clearing/house/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0755
        }
    ]

    def check_command(self):
        if self.last_user_input == "ls":
            return
        return StepTemplateChmod.check_command(self)

    def next(self):
        Step14()


class Step14(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:The command is}} {{yb:rm}}{{Bb:.}}",
        "{{Bb:Let's test this. It's dangerous to use this in the house, so let's go outside first.}}",
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing"
    commands = [
        "cd ..",
        "cd ../"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step16()


class Step16(StepTemplateChmod):
    story = [
        "Look around to decide what to remove."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step17()


class Step17(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:Let's remove the weed with}} {{yb:rm weed}}{{Bb:.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "rm weed"
    ]

    def block_command(self):
        # TODO probably need to unblock rm
        return StepTemplateChmod.block_command(self)

    def next(self):
        Step18()


class Step18(StepTemplateChmod):
    story = [
        "Look around to confirm you removed the weed."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]

    def next(self):
        Step19()


class Step19(StepTemplateChmod):
    story = [
        "Swordmaster: {{Bb:You're ready to face the rabbit}}",
        "{{Bb:Let's head to the rabbithole together.}}",
        "{{Bb:Lead me to it.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/thicket"

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step1()


# Story where swordmaster gets kidnapped by the rabbit
class Step2(StepTemplateChmod):
    print_text = REPLY_PRINT_TEXT
    # story = SWORDMASTER_STORY + [
    #     "",
    #     "{{pb:Ding. Dong.}}"
    # ]
    story = [
        "{{pb:Ding. Dong.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls .",
        "ls ./"
    ]
    hints = [
        "Look around with {{yb:ls}}"
    ]
    # story_dict = {
    #     "RM-sword": {
    #         "name": "sword",
    #         "path": "~/town/east/library/private-section"
    #     },
    #     "torn-note": {
    #         "path": "~/town/east/library/private-section"
    #     }
    # }
    file_list = [
        {
            "path": "~/town/east/library/private-section/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0644
        }
    ]

    deleted_items = ["~/town/east/library/private-section/swordmaster"]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "The swordmaster has gone.",
        "",
        "He left something behind. It looks like the {{lb:sword}} he carries around with him.",
        "Examine it closely."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "cat sword"
    ]

    hints = [
        "Use {{yb:cat sword}} to examine it."
    ]

    def next(self):
        Step4()


class Step4(StepTemplateRm):
    story = [
        "It has a command inscribed on it.",
        "....{{lb:rm}}...?",
        "",
        "Use this command on that {{lb:torn-note}} to see what it does.",
        "Be careful though....it looks dangerous."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "rm torn-note"
    ]

    hints = [
        "",
        "Use the command {{lb:rm torn-note}}"
    ]

    def next(self):
        Step5()


class Step5(StepTemplateRm):
    story = [
        "Look around"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls"
    ]

    hints = [
        "Use the command {{lb:ls}}"
    ]

    def next(self):
        NextStep()
