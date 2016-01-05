#!/usr/bin/env python
#
# Copyright (C) 2014, 2015, 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
import time
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateChmod(TerminalChmod):
    challenge_number = 41


# The note says:
# "Hello. I here to help you.
# Show me where you think the Super User command is kept."
class Step1(StepTemplateChmod):
    story = [
        "The Rabbit wants to know where the Super User command is kept?",
        "....",
        "Oh! Could it be in the locked section of the library?",
        "Let's head there. I guess the Rabbit will follow."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/town/east/library"
    hints = [
        "{{rb:Use}} {{yb:cd ~/town/east/library}} {{rb:to go to the library}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


# Make the rabbit follow whether the user goes.
# If the user does cat rabbit, the rabbit should reply with his emotions
# depending on how far he is from the locked room
class Step2(StepTemplateChmod):
    story = [
        "Now, which is the locked room? {{lb:Look around}} to remind yourself."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    story_dict = {
        "Rabbit": {
            "path": "~/town/east/library"
        }
    }
    deleted_items = ["~/woods/thicket/.raabithole/Rabbit"]

    def next(self):
        Step3()


class Step3(StepTemplateChmod):
    story = [
        "Ah, it's the {{lb:private-section}}.",
        "The Rabbit looks very excited. His eyes are sparkling.",
        "How do you unlock the {{lb:private-section}}? It was the command "
        "that the swordsmaster talked about..."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library"
    commands = [
        "chmod +rwx private-section",
        "chmod +rwx private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/",
        "chmod +xrw private-section",
        "chmod +xrw private-section/",
        "chmod +rxw private-section",
        "chmod +rxw private-section/",
        "chmod +xwr private-section",
        "chmod +xwr private-section/",
        "chmod +wxr private-section",
        "chmod +wxr private-section/"
    ]

    hints = [
        "{{rb:The command was}} {{lb:chmod}}{{rb:, and you need to enable "
        "all the permissions.}}",
        "{{rb:The command is}} {{yb:chmod +rwx private-section}} {{rb:to "
        "make the private-section readable, "
        "writeable and executable so you can go inside.}}"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateChmod):
    story = [
        "Awesome, you unlocked it! Let's go inside."
    ]
    start_dir = "~/town/east/library"
    end_dir = "~/town/east/library/private-section"
    hints = [
        "{{rb:Use}} {{yb:cd private-section/}} {{rb:to go inside the}} "
        "{{rb:private-section.}}"
    ]
    story_dict = {
        "SUDO": {
            "path": "~/town/east/library/private-section"
        }
    }

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step5()


class Step5(StepTemplateChmod):
    story = [
        "Have a look around."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls -a"
    ]
    story_dict = {
        "Rabbit": {
            "path": "~/town/east/library/private-section"
        }
    }
    deleted_items = ["~/town/east/library/Rabbit"]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step6()


class Step6(StepTemplateChmod):
    story = [
        "You see a piece of paper with {{lb:SUDO}} written on it.",
        "It looks like another command. Read it."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "cat SUDO"
    ]
    hints = [
        "{{rb:Read the note with}} {{yb:cat SUDO}}{{rb:.}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateChmod):
    story = [
        "This looks like the command we were looking for.",
        "The Rabbit looks more excited than you've ever seen "
        "him before.",
        "He snatches the paper off you and runs off!",
        "{{gb:Press ENTER to continue.}}"
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"

    def next(self):
        script_path = os.path.expanduser("~/terminal-quest/bin/rabbit")
        os.system(script_path)

        self.exit()
        time.sleep(3)
