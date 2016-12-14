#!/usr/bin/env python
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
import os

import time

from linux_story.Animation import Animation
from linux_story.common import get_username, get_story_file
from linux_story.step_helper_functions import unblock_cd_commands
from linux_story.story.terminals.terminal_sudo import TerminalSudo


class StepTemplateSudo(TerminalSudo):
    challenge_number = 50

REPLY_PRINT_TEXT = ["A rabbit came and stole the command in front of us."]
SWORDMASTER_STORY = [
        "Swordmaster: {{Bb:I see.}}",
        "{{Bb:You idiot. Did you bring the rabbit with you?}}",
        "{{Bb:I met a white rabbit before, but It was an innocent creature then.}}",
        "{{Bb:Perhaps he is}} {{lb:possessed}}{{Bb.}}",
        "{{Bb:We must remove the source of the problem. I will teach you how to.}}"
]

class Step10(StepTemplateSudo):
    story = [
        "You are standing alone in the library. The rabbit has stolen the command, and you have an increased sense of "
        "impending doom.",
        "You see the swordmaster run into the room.",
        "Swordmaster: {{Bb:What have you done?}}",
        "",
        "{{yb:1: A rabbit came and stole the command in front of us.}}",
        "{{yb:2: Nothing.}}",

    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
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

    # def check_command(self):
    #     if self.last_user_input in self.extra_hints:
    #         self.send_hint(self.extra_hints[self.last_user_input])
    #     return StepTemplateSudo.check_command(self)

    def next(self):
        if self.last_user_input == "echo 1":
            Step21()
        else:
            StepAngrySwordMaster(user_reply=self.user_replies[self.last_user_input])


class StepAngrySwordMaster(StepTemplateSudo):
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
        StepTemplateSudo.__init__(self)

    def next(self):
        if self.last_user_input == "echo 1":
            Step21()
            # Step11()
            # or Step21() or get the ending where the rabbit kills the swordmaster
        else:
            GameOver()


class GameOver(StepTemplateSudo):
    story = [
        "Swordmaster: {{Bb:You stole it, didn't you?",
        "Then it's time to end this.}}"
    ]

    def next(self):
        self.send_hint("Game over!")
        time.sleep(3)
        self.exit()


class Step11(StepTemplateSudo):
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


class Step12(StepTemplateSudo):
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


class Step13(StepTemplateSudo):
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
    # {
    #     "swordmaster-without-sword": {
    #         "name": "swordmaster",
    #         "path": "~/woods/clearing/house"
    #     },
    #     "RM-sword": {
    #         "name": "sword",
    #         "path": "~/woods/clearing/house"
    #     }
    # }

    def check_command(self):
        if self.last_user_input == "ls":
            return
        return StepTemplateSudo.check_command(self)

    def next(self):
        Step14()


class Step14(StepTemplateSudo):
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


class Step16(StepTemplateSudo):
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


class Step17(StepTemplateSudo):
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
        return StepTemplateSudo.block_command(self)

    def next(self):
        Step18()


class Step18(StepTemplateSudo):
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


class Step19(StepTemplateSudo):
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
class Step21(StepTemplateSudo):
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
            "path": "~/town/east/library/private-section/swordmaster",
            "contents": get_story_file("swordmaster-without-sword"),
            "type": "file",
            "permissions": 0644
        },
        {
            "path": "~/town/east/library/private-section/sword",
            "contents": get_story_file("RM-sword"),
            "type": "file",
            "permissions": 0644
        }
    ]

    def next(self):
        Step22()


class Step22(StepTemplateSudo):
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
        Step23()


class Step23(StepTemplateSudo):
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
        Step24()


class Step24(StepTemplateSudo):
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
        Step25()


class Step25(StepTemplateSudo):
    story = [
        "You destroyed the torn-note.",
        "The rm command gives you the power to {{lb:remove}} items.",
        "",
        "It is time to find that rabbit.",
        "Go to where you met the rabbit."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/thicket"

    hints = [
        "Remember where you met the rabbit?",
        "You met the rabbit in the woods",
        "Go to ~/woods/thicket"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step26()


class Step26(StepTemplateSudo):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "ls",
        "ls .",
        "ls ./",
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    hint = [
        "Use ls to look around"
    ]

    def next(self):
        Step1()


# Outside the rabbithole.
class Step1(StepTemplateSudo):
    story = [
        "You are outside the rabbithole. Try and go inside."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]
    # story_dict = {
    #     "rabbithole": {
    #         "path": "~/woods/thicket",
    #         "permissions": 0000
    #     }
    # }
    file_list = [
        {
            "type": "directory",
            "path": "~/woods/thicket/rabbithole",
            "permissions": 0000
        }
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateSudo):
    story = [
        "It looks like it is locked to us. The rabbit must have learnt how to lock the directory",
        "Unlock it."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"

    commands = [
        # wrap this in a function?
        "chmod +rwx rabbithole",
        "chmod +rwx rabbithole/",
        "chmod +rxw rabbithole",
        "chmod +rxw rabbithole/",
        "chmod +wxr rabbithole",
        "chmod +wxr rabbithole/",
        "chmod +wrx rabbithole",
        "chmod +wrx rabbithole/",
        "chmod +xwr rabbithole",
        "chmod +xwr rabbithole/",
        "chmod +xrw rabbithole",
        "chmod +xrw rabbithole/"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateSudo):
    story = [
        "Now go inside"
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "cd rabbithole",
        "cd rabbithole/"
    ]

    # story_dict = {
    #     "bell, Rabbit": {
    #         "path": "~/woods/thicket/rabbithole"
    #     },
    #     # these should be moved as in appropriate in the story
    #     "Mum, Dad, dog, Edith, Edward, grumpy-man, Mayor, young-girl, little-boy": {
    #         "path": "~/woods/thicket/rabbithole/cage"
    #     }
    # }
    file_list = [
        {
            "path": "~/woods/thicket/rabbithole/bell",
            "type": "file",
            "contents": get_story_file("bell"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/Rabbit",
            "type": "file",
            "contents": get_story_file("Rabbit"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mum",
            "type": "file",
            "contents": get_story_file("Mum"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Dad",
            "type": "file",
            "contents": get_story_file("Dad"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/dog",
            "type": "file",
            "contents": get_story_file("dog"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edith",
            "type": "file",
            "contents": get_story_file("Edith"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Edward",
            "type": "file",
            "contents": get_story_file("Edward"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/grumpy-man",
            "type": "file",
            "contents": get_story_file("grumpy-man"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/Mayor",
            "type": "file",
            "contents": get_story_file("Mayor"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/young-girl",
            "type": "file",
            "contents": get_story_file("young-girl"),
            "permissions": 0644
        },
        {
            "path": "~/woods/thicket/rabbithole/cage/little-boy",
            "type": "file",
            "contents": get_story_file("little-boy"),
            "permissions": 0644
        }
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplateSudo):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"

    commands = [
        "ls",
        "ls ./",
        "ls ."
    ]

    def next(self):
        Step5()


class Step5(StepTemplateSudo):
    story = [
        "You see the rabbit in front of you, a cage and a mysteriously glowing bell. Investigate."
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    hints = [""]  # don't show hints for this section
    allowed_places = ["~/woods/thicket/rabbithole"]
    commands_done = {
        "cat bell": False,
        "cat Rabbit": False
    }

    def check_command(self):
        story = ""
        if self.last_user_input == "cat Rabbit":
            story = "Rabbit: {{Bb:...}}\nThe rabbit looks frustrated."
        if self.last_user_input == "cat bell":
            story = "The bell glows menacingly."
        if self.last_user_input.startswith("cat cage/"):
            story = self.cat_people()
        self.send_hint(story)

        if self.last_user_input in self.commands_done:
            self.commands_done[self.last_user_input] = True

        for command in self.commands_done:
            if not self.commands_done[command]:
                return False

        return True

    def cat_people(self):
        people = {
            "Mum": "Mum: {{Bb:" + get_username() + ", I'm so glad to see you're safe!}}",
            "Dad": "Dad: {{Bb:Caught by a rabbit!}}",
            "grumpy-man": "grumpy-man: {{Bb:I hope my wife knows I'm safe.}}",
            "Mayor": "Mayor: {{Bb:I'm going to bring in a law to hunt all rabbits}}",
            "little-boy": "little-boy: {{Bb:I miss my mummy!}}",
            "young-girl": "young-girl: {{Bb:I miss my mummy!}}",
            "Edith": "Edith: {{Bb:You! Get us out of here!}}",
            "Edward": "Edward: {{Bb:Edith dear, calm down...}}",
            "dog": "dog: {{Bb:Woof woof!}}",
            "head-librarian": "head-librarian: {{Bb:Who are you?}}"
        }
        for person in people:
            if self.last_user_input == "cat cage/" + person:
                return people[person]

        return ""

    def next(self):
        Step7()


class Step7(StepTemplateSudo):
    story = [
        "Swordmaster: {{Bb:What are you waiting for?",
        "You need to}} {{yb:remove the source of the problem.}}"
    ]
    start_dir = "~/woods/thicket/rabbithole"
    end_dir = "~/woods/thicket/rabbithole"
    commands = [
        "rm bell"
    ]

    def block_command(self):
        if self.last_user_input == "rm Rabbit":
            self.send_hint("Swordmaster: {{Bb:I don't think that is the source of the problem...}}")
            return True
        return StepTemplateSudo.block_command(self)

    def next(self):
        print self.last_user_input
        # TODO play animation of the bell being destroyed?
        # Then the rabbit blinking, and the text of the rabbit saying ""
        Animation("firework-animation").play_finite(cycles=1)
        self.send_hint("Done!")

