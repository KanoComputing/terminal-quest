#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_nano import TerminalNano
from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands, unblock_commands_with_cd_hint
)
from linux_story.story.challenges.challenge_35 import Step1 as NextStep


class StepTemplateNano(TerminalNano):
    challenge_number = 34


class StepTemplateChmod(TerminalChmod):
    challenge_number = 34


class Step1(StepTemplateNano):
    story = [
        "{{wb:Cluck.}} {{yb:It sounds like the door unlocked.}}",
        "Go inside."
    ]

    # Change permissions of the house directory here.
    start_dir = "~/woods/clearing"

    # This should be an array of allowed directories you can end up in.
    # Perhaps an empty array means it doesn't matter where you end up.
    end_dir = "~/woods/clearing/house"

    # Level up based on the output of the command.

    hints = [
        "{{rb:Use}} {{yb:cd house/}} {{rb:to go into the house.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    # Perhaps a nice data structure could be if the list of commands were
    # paired with appropriate hints?

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "You see a masked swordsmaster watching you.",
        "Listen to what he has to say."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cat swordsmaster}} {{rb:to}} {{lb:listen}} "
        "{{rb:to what the swordsmaster has to say.}}"
    ]
    commands = [
        "cat swordsmaster"
    ]

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "{{wb:Swordsmaster:}} {{Bb:Child, why do you seek me?}}",
        "{{yb:1: How did you lock your front door?}}",
        "{{yb:2: Who are you?}}",
        "{{yb:3: Have you been leaving me the strange notes?}}",
        "",
        "Respond with {{yb:echo 1}} {{yb:echo 2}} or {{yb:echo 3}}."
    ]
    commands = [
        "echo 1"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}}{{rb:.}}"
    ]
    extra_hints = {
        "echo 2": "Swordsmaster: {{Bb:That is none of your business.}}",
        "echo 3": "Swordsmaster: {{Bb:What notes?}}"
    }

    def check_command(self):

        if self.last_user_input in self.extra_hints:
            hint = self.extra_hints[self.last_user_input]
            self.send_hint(hint)

        return StepTemplateNano.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    print_text = [
        "{{yb:How did you lock your front door?}}"
    ]
    story = [
        "Swordsmaster: {{Bb:I used a special command. Only those who have "
        "proved themselves may learn it.",
        # How does he know your name? Initially thought of ls -l.
        "I know of your name...it is written all over this world for those "
        "who know where to look.",
        # ...but are you who you say you are? I want to see what you know!
        "...Ok. I will teach how I lock my door and protect myself.",
        # "First, try and {{lb:look inside}} my basement."
        "First, try and}} {{lb:go inside}} {{Bb:my basement.}}"
    ]
    # This logic for commands doesn't work
    commands = [
        "cd basement",
        "cd basement/"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Use}} {{yb:cd basement/}} {{rb:to look in the basement.}}"
    ]
    needs_sudo = True

    def check_command(self):
        if self.last_user_input.strip() in self.commands:
            print "-bash: cd: basement: Permission denied"
            return True

    def block_command(self):
        if self.last_user_input.startswith("cd"):
            return True

    def next(self):
        Step6()


# Make directory executable
class Step6(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You got the error}} {{yb:-bash: cd: basement: Permission denied}}",
        "{{Bb:This directory is missing all its permissions.}}",
        "{{Bb:They normally have three.}}",
        "{{Bb:To go inside, you need the make the directory eXecutable.}}",
        "{{Bb:Use}} {{yb:chmod +x basement}} {{Bb:to unlock the basement.}}"
    ]
    commands = [
        "chmod +x basement",
        "chmod +x basement/"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"

    def next(self):
        Step7()


class Step7(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Well done. Now go inside the basement.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house/basement"
    commands = [
        "cd basement",
        "cd basement/"
    ]

    def block_command(self):
        return unblock_commands_with_cd_hint(self.last_user_input,
                                             self.commands)

    def next(self):
        Step8()


class Step8(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Look around.}}"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"
    commands = [
        "ls", "ls -a"
    ]

    def next(self):
        Step9()


# Readable
class Step9(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:You got the error}} {{yb:ls: cannot open directory .: Permission denied}}",
        "{{Bb:This is because you do not have Read Access to this directory.",
        "You need to force the Read permissions using the +r flag.}} "
        "{{Bb:Try the command}} {{yb:chmod +r ./}} {{Bb:to add the "
        "ability to Read.}}"
    ]
    commands = [
        "chmod +r .",
        "chmod +r ./"
    ]
    hints = [
        "{{rb:Use}} {{yb:chmod +r ./}} {{rb:to change the permissions on the basement.}}"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    def next(self):
        Step10()


class Step10(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Now try and}} {{lb:look around}} {{Bb:}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    start_dir = "~/woods/clearing/house/basement"
    end_dir = "~/woods/clearing/house/basement"

    hints = [
        "{{rb:Look in the basement using}} {{yb:ls}}"
    ]

    def next(self):
        NextStep(self.xp)
