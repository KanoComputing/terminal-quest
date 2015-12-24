#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.terminals.terminal_sudo import TerminalSudo
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands, unblock_commands_with_mkdir_hint
)
from linux_story.story.challenges.challenge_37 import Step1 as NextStep


class StepTemplateChmod(TerminalChmod):
    challenge_number = 36


class StepTemplateSudo(TerminalSudo):
    challenge_number = 36


# Note reads:
# We need to find a special command which makes the User into a Super User.
# I'm close, look for me more closely.
class Step1(StepTemplateChmod):
    story = [
        "Look more closely? Ok, let's {{lb:look more closely}}."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls -a}} {{rb: to look around more closely.}}"
    ]

    def next(self):
        Step20()


class Step20(StepTemplateChmod):
    story = [
        "There's a .rabbithole! Let's go inside."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket/.rabbithole"
    hints = [
        "{{rb:Use}} {{yb:cd .rabbithole/}} {{rb:to go inside.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step21()


class Step21(StepTemplateChmod):
    story = [
        "Look around"
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around more closely.}}"
    ]

    def next(self):
        Step22()


class Step22(StepTemplateChmod):
    story = [
        "You see a Rabbit, a piece of paper and a doorway.",
        "This Rabbit looks somewhat familiar...",
        "{{lb:Listen}} to the Rabbit."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "cat Rabbit"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat Rabbit}} {{rb:to examine the Rabbit.}}"
    ]

    def next(self):
        Step23()


class Step23(StepTemplateChmod):
    story = [
        "Rabbit: {{Bb:...}}",
        "It seems the Rabbit doesn't say very much. Presumably that's quite "
        "normal for rabbits.",
        "Let's read the {{lb:note}}."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "cat note"
    ]
    hints = [
        "{{rb:Use}} {{yb:cat note}} {{rb:to read the note.}}"
    ]

    def next(self):
        Step24()


# The note says:
# "Hello. I here to help you.
# Show me where you think the Super User command is kept."
class Step24(StepTemplateChmod):
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
        Step25()


# Make the rabbit follow whether the user goes.
# If the user does cat rabbit, the rabbit should reply with his emotions
# depending on how far he is from the locked room
class Step25(StepTemplateChmod):
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

    def next(self):
        Step26()


class Step26(StepTemplateChmod):
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
        "{{rb:Think back to the swordsmasters lesson...you need to make}} "
        "{{rb:the}} {{lb:private-section}} {{rb:both}} {{yb:readable}} "
        "{{rb:and}} {{yb:writeable}}{{rb:, and go inside.}}",
        "{{rb:The command was}} {{lb:chmod}}{{rb:. What are the addtional "
        "parameters?}}",
        "{{rb:The command is}} {{yb:chmod +rwx private-section}} {{rb:to "
        "make the}} {{lb:private-section}} {{rb:both readable, "
        "writeable and executable so you can go inside.}}"
    ]

    def next(self):
        Step27()


class Step27(StepTemplateChmod):
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
        Step28()


class Step28(StepTemplateChmod):
    story = [
        "Have a look around."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/town/east/library/private-section"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step29()


class Step29(StepTemplateChmod):
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
        Step30()


# Fork where the rabbit finds out the password.
'''
# We could skip this part and say the rabbit doesn't know the password.
class Step30(StepTemplateChmod):
    story = [
        "This commands says it makes the user into a Super User, and allows "
        "them to do things they couldn't do before.",
        "This looks like the command the Rabbit was looking for.",
        "His eyes are glistening. Maybe you should try it out?",
        # What can the user do that was impossible before?
        # Perhaps we see an immoveable rock near the swordsmaster, and we
        # go back there to see if we can use sudo mv.
        # Manually change the ls -l
        "Remember that immoveable rock we saw in the woods?",
        "Let's see if we have the power to move it!",
        "Let's go to the {{lb:woods}}."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods"

    def next(self):
        Step31()


# We could do a play on the sword and the stone. Only the hero will remove the
# sword in the stone.
class Step31(StepTemplateChmod):
    story = [
        "Try and move the rock to {{lb:../}}"
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "mv rock ../"
    ]

    def next(self):
        Step32()


class Step32(StepTemplateChmod):
    story = [
        "Hm...that didn't work.",
        "Let's now try doing {{yb:sudo mv rock ../}} to see if that will give "
        "us the extra power."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods"
    commands = [
        "sudo mv rock ../"
    ]

    def next(self):
        Step33()


class Step33(StepTemplateChmod):
    story = [
        "That worked!",
        "The Rabbit looks much more excited then you think you've ever seen "
        "him before. For the first time, you notice a big gong that he has on "
        "his back...",
        "He snatches the paper off you and runs off!"
        # Show curses animation
        "So that's where you've seen him before!",
        "That's the rabbit that tried to blow you up on the desktop!",
        "He's the monster that's been kidnapping everyone!",
        "We need to defeat him. But how?",
        "Perhaps the mysterous swordsmaster can help.",
        "Let's head to his house."
    ]
    start_dir = "~/woods"
    end_dir = "~/woods/clearing/house"

    def next(self):
        Step34()
'''


class Step30(StepTemplateChmod):
    story = [
        "This looks like the command we were looking for.",
        "The Rabbit looks more excited than you've ever seen "
        "him before.",
        "He snatches the paper off you and runs off!",
        # Show curses animation
        "That's the rabbit that tried to blow you up on the desktop!",
        "Is he the monster that's been kidnapping everyone?",
        "Perhaps the mysterous swordsmaster can help.",
        "Let's head to his house."
    ]
    start_dir = "~/town/east/library/private-section"
    end_dir = "~/woods/clearing/house"

    # Can we do hints based on current location?
    # Should we go directly to the house, or go to the clearing, and then do a
    # special password to get quick access?
    hints = [
        "{{rb:Use}} {{yb:cd ~/woods/clearing/house}} {{rb:to jump straight to "
        "the swordsmaster's house.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step33()


class Step33(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to look around.}}"
    ]

    def next(self):
        Step33b()


class Step33b(StepTemplateChmod):
    story = [
        "The swordsmaster looks surprised to see you. {{lb:Listen to him.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "cat swordsmaster"
    ]
    hints = [
        "{{rb:Listen to the swordsmaster with}} {{yb:cat swordsmaster}}"
    ]

    def next(self):
        Step34()


class Step34(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:What are you doing back here so soon?",
        "...you look worried. What's happened child?}}",
        "{{yb:1: I found the sudo command in the library.",
        # If you do this too much, the swordsmaster kills you.
        "2: I'm now invincible, bow before me.}}"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "echo 1",
    ]
    hints = [
        "{{rb:Use}} {{yb:echo 1}} {{rb:or}} {{yb:echo 2}} {{rb:.}}"
    ]

    def next(self):
        Step35()


# Assume echo 1
class Step35(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:.....I hid that a long time ago.",
        "I told the librarians to guard it and keep it safe.",
        "They knew it was important no one go there.",
        "Tell me - did you tell anyone else about it?}}",
        "{{yb:1: Yes. A white rabbit that promised to help me.",  # progress
        "2: I was tricked by a white rabbit.",  # progress
        "3: No I did not.}}"
        # Swordsmaster: ...you're not tellling me something. Be honest with me.
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    hints = [
        "{{rb:Reply with}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:or}} "
        "{{yb:echo 3}}{{rb:.}}"
    ]

    commands = [
        "echo 1",
        "echo 2"
    ]

    def next(self):
        Step36()


class Step36(StepTemplateChmod):
    story = [
        "The swordsmaster starts rapidly pacing.",
        "Swordsmaster: {{Bb:A white rabbit?",
        "I've heard rumors about such a creature. A silent creature with a "
        "corrupt heart.",
        "We might be in luck - this command needs a password to work.",
        "Tell me, and be completely straight with me. Does the rabbit know "
        "the password?}}",
        "{{yb:1: Yes}}",  # ....I hope you are joking. Otherwise we're all dead.
        "{{yb:2: No}}",
        "{{yb:3: I don't know}}"  # Reply to this with "Did you tell the rabbit the password?"
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing/house"
    commands = [
        "echo 2",
    ]

    def next(self):
        Step37()


class Step37(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:Ok we might have time then."
        "...we need to hurry.}}",
        "",
        "The swordsmaster leaves the house and goes to the clearing. Follow him."
    ]
    start_dir = "~/woods/clearing/house"
    end_dir = "~/woods/clearing"
    hints = [
        "{{rb:Go back a directory using}} {{yb:cd ../}}"
    ]

    deleted_items = ["~/woods/clearing/house/swordsmaster"]
    story_dict = {
        "swordsmaster": {
            "path": "~/woods/clearing/house"
        }
    }

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step38()


class Step38(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:There is an object I found in my travels.",
        "It has special permissions.}} {{lb:Look around}}{{Bb:, it is in this"
        " clearing.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{lb:to look around.}}"
    ]

    def next(self):
        Step39()


# What is wrong with the sword?
# Or, do we have some sort of "immoveable rock?"
# It could be really really really heavy?
class Step39(StepTemplateChmod):
    story = [
        "You see a strange {{lb:chest}}.",
        "",
        "Swordsmaster: {{Bb:This chest is locked.}}",
        "{{lb:Try and open it.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "chmod +wr chest",
        "chmod +wr chest/",
        "chmod +rw chest",
        "chmod +rw chest/"
    ]
    hints = [
        "{{rb:Use}} {{yb:chmod +rw chest/}} {{rb:to unlock the chest.}}"
    ]

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextStep(self.xp)
