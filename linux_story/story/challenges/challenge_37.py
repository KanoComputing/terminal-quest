#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_chmod import TerminalChmod
from linux_story.story.terminals.terminal_rm import TerminalRm
from linux_story.story.terminals.terminal_sudo import TerminalSudo
from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands
)
import getpass
import time


class StepTemplateChmod(TerminalChmod):
    challenge_number = 37


class StepTemplateRm(TerminalRm):
    challenge_number = 37


class StepTemplateSudo(TerminalSudo):
    challenge_number = 37


class Step1(StepTemplateSudo):
    story = [
        "It didn't work. You found that you didn't have the permissions to "
        "move it",
        "Swordsmaster: {{Bb:This is where the power of sudo comes in.",
        "sudo allows you to do what Super User can do.",
        "However you need to know the system secret password.",
        "I need you to prove you yourself. You must guess the password.}}"
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"

    # How to prevent this happening if you DON'T do sudo.
    commands = [
        "sudo chmod +rw chest",
        "sudo chmod +rw chest/",
        "sudo chmod +wr chest",
        "sudo chmod +wr chest/"
    ]

    def next(self):
        Step41()


class Step41(StepTemplateSudo):
    story = [
        "Swordsmaster: {{Bb:...well done.",
        "You've nearly ready to defeat the Rabbit.",
        "You just need one more command. This is the most dangerous of them "
        "all.",
        "Just...don't tell anyone about this.}}",
        "The swordsmaster takes a note out of his pocket and give it to you.",
        "Swordsmaster: {{Bb:Look around to see it.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:look at what the swordsmaster dropped.}}"
    ]
    story_dict = {
        "RM": {
            "path": "~/woods/clearing",
        }
    }

    def next(self):
        Step42()


class Step42(StepTemplateChmod):
    story = [
        "The note the swordsmaster is called RM.",
        "{{lb:Read}} it to see what it says."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "cat RM",
    ]
    hints = [
        "{{rb:Use}} {{yb:cat RM}} {{lb:to read the note.}}"
    ]

    def next(self):
        Step43()


class Step43(StepTemplateRm):
    story = [
        "Swordsmaster: to use it, try now removing an object in the clearing.",
        "This is irreversible. You should only do this if you are absolutely "
        "sure.",
        "See that weed? No one likes weeds. Use {{yb:rm weed}} to remove it."
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "rm weed"
    ]
    hints = [
        "{{rb:Use}} {{yb:rm weed}} {{rb:to remove the weed.}}"
    ]

    def next(self):
        Step47()


'''
class Step44(StepTemplateRm):
    story = [
        "Swordsmaster: {{Bb:Now for the ultimate test. Let's try that "
        "stone. Use the command}} {{lb:sudo rm hole/stone}} {{Bb:to remove "
        "the stone.}}"
    ]
    start_dir = "~/woods/clearing"
    end_dir = "~/woods/clearing"
    commands = [
        "sudo rm hole/stone"
    ]
    hints = [
        "{{rb:Use}} {{yb:sudo rm hole/stone}} {{rb:to attempt to remove the "
        "stone.}}"
    ]

    def next(self):
        Step47()
'''


class Step47(StepTemplateChmod):
    story = [
        "The swordsmaster looks at you with apprehension.",
        "Swordsmaster: {{Bb:Well done. You hold a lot of power. Be very "
        "careful where you use this. You can cause great damage.",
        "Now! Time to face your enemy. Where do you think he is?}}",
        "",
        "Let's head back to the rabbithole to see if we can find the rabbit."
    ]

    start_dir = "~/woods/clearing"
    end_dir = "~/woods/thicket/.rabbithole"

    def block_command(self):
        return self.unblock_cd_commands(self.last_user_input)

    def next(self):
        Step48()


class Step48(StepTemplateChmod):
    story = [
        "Look around to see where to go next."
    ]

    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Use}} {{yb:ls}} {{rb:to decide where to go next.}}"
    ]

    def next(self):
        Step49()


# You could also see a note telling you to keep away.
class Step49(StepTemplateChmod):
    story = [
        "You see a note.",
        "{{lb:Read}} the note."
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
        Step50()


# if the directory is executable
# TODO: how to block cd commands
class Step50(StepTemplateChmod):
    story = [
        "Swordsmaster: {{Bb:He is trying to intimidate you.",
        "If he knew the password he would not be playing these mind games.}}",
        "",
        "You see a doorway ahead of you.",
        "Head inside."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:cd doorway}} {{rb:to go inside the doorway.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step52()


class Step52(StepTemplateChmod):
    story = [
        "You don't have permissions to go inside.",
        "It looks like the rabbit has locked the doorway.",
        "Do you remember how to unlock it?",
        "Remember - we need to make the directory both Readable (to see "
        "what's inside), and also Writable, as we plan to change the contents "
        "of it."
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole"
    commands = [
        "chmod +rw doorway",
        "chmod +rw doorway/"
    ]
    # We could take the approach here where we have some tests, and if they pass, the user has probably doen the right thing
    # Otherwise, just check base don command.
    hints = {
        "chmod +r doorway": "This will mean that you can't change the "
        "contents of the directory",
        "chmod +w doorway": "This will mean that you can't see what is inside "
        "the directory"
    }

    def next(self):
        Step53()


class Step53(StepTemplateChmod):
    story = [
        "Now go inside"
    ]
    start_dir = "~/woods/thicket/.rabbithole"
    end_dir = "~/woods/thicket/.rabbithole/doorway"

    hints = [
        "{{rb:Use}} {{yb:cd doorway}} {{rb:to go inside the doorway.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step54()


class Step54(StepTemplateChmod):
    story = [
        "Look around."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"

    def next(self):
        Step55()


class Step55(StepTemplateChmod):
    story = [
        # the rabbit could discover the password as you walk in.
        "You are in a dank basement. You see the Rabbit, a cage, and the "
        "SUDO paper now crumpled and covered in pawprints.",
        "From within the cage you hear murmuring.",
        "There is a rabbithutch that looks perfect to contain the rabbit..."
        "The Rabbit looks very frustrated and angry.",
        "Swordsmaster: {{Bb:Now is your chance! Move the Rabbit to the "
        "rabbithutch!}}"
    ]
    hints = {
        "{{rb:Use}} {{yb:mv Rabbit rabbithutch}} {{rb:to move the Rabbit to "
        "the rabbithutch}}"
    }
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    commands = [
        "mv Rabbit rabbithutch/",
        "mv Rabbit rabbithutch"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.commands)

    def next(self):
        # If you don't kill the rabbit straight away, you should hit a
        # gameover screen.
        Step56()


class Step56(StepTemplateSudo):
    story = [
        "Now lock it! Use {{lb:sudo chmod -rw rabbithutch/}}"
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = {
        "{{rb:Use}} {{yb:sudo chmod -rw rabbithutch}} {{yb:to stop the "
        "rabbit leaving. You need sudo, otherwise the rabbit can unlock the "
        "hutch.}}"
    }
    commands = [
        "sudo chmod -rw rabbithutch/",
        "sudo chmod -rw rabbithutch",
        "sudo chmod -wr rabbithutch/",
        "sudo chmod -wr rabbithutch"
    ]

    def next(self):
        # If you don't kill the rabbit straight away, you should hit a
        # gameover screen.
        Step57()


class Step57(StepTemplateSudo):
    story = [
        "You've locked the rabbit away! Now let's look in the cage."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:ls cage/}}"
    ]
    commands = [
        "ls cage/",
        "ls cage"
    ]

    def next(self):
        Step58()


class Step58(StepTemplateSudo):
    story = [
        "You see all the people who went missing.",
        "Is your Mum here? Check how she is."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:cat cage/Mum}} {{rb:to check how she is.}}"
    ]
    commands = [
        "cat cage/Mum"
    ]

    def next(self):
        Step59()


class Step59(StepTemplateSudo):
    username = getpass.getuser()
    story = [
        "Mum: {{Bb:" + username + ", is that you? Oh it's so good to see you!",
        "We're trapped in here! Do you know how to let us out?}}"
        "Unlock the cage with {{yb:chmod +w cage/}}"
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:chmod +w cage/}} {{rb:to unlock the cage.}}"
    ]
    commands = [
        "chmod +w cage/",
        "chmod +w cage"
    ]

    def next(self):
        Step60()


class Step60(StepTemplateSudo):
    story = [
        "Everyone leaves the cage and rabbithole.",
        "One person called {{yb:Judoka}} remains.",
        "He looks like he wants to talk to you.",
        "Listen to him."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:cat Judoka}} {{rb:to listen to Judoka.}}"
    ]
    commands = [
        "cat Judoka"
    ]

    def next(self):
        Step61()


class Step61(StepTemplateSudo):
    story = [
        "Judoka: {{Bb:Thank you for saving everyone. The Rabbit is my pet, "
        "but while I was modifying its hutch, it changed directory and got "
        "modified. I think I corrupted it's heart and made it evil. "
        "It then trapped me in its cage!"
        "I had time to think about how to solve it - I think this script "
        "should fix it. I have it here.}}",
        "{{Bb:First we need to move it into the rabbithutch so it next to the rabbit.}}"
        "Run {{yb:sudo mv fix-rabbit-script.sh rabbithutch/}} - use sudo to "
        "make sure the script moves into the rabbithutch."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Run}} {{yb:sudo mv fix-rabbit-script.sh rabbithutch/}} "
        "to move the script into the rabbithutch."
    ]
    commands = [
        "sudo mv fix-rabbit-script.sh rabbithutch",
        "sudo mv fix-rabbit-script.sh rabbithutch/"
    ]

    def next(self):
        Step62()


class Step62(StepTemplateSudo):
    story = [
        "Judoka: {{Bb:Now run it! Use}} "
        "{{yb:sudo ./rabbithutch/fix-rabbit-script.sh}}"
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Run}} {{yb:sudo ./rabbithutch/fix-rabbit-script.sh}} "
        "to run the script."
    ]
    commands = [
        "sudo ./rabbithutch/fix-rabbit-script.sh"
    ]

    def next(self):
        Step63()


class Step63(StepTemplateSudo):
    story = [
        "Judoka: {{Bb:...now time to see if it worked.}}",
        "{{Bb:Unlock the cage.}}",
        "",
        "Swordsmaster: {{Bb:}}...If this goes wrong, be ready to remove "
        "the Rabbit.}}",
        "",
        "Use {{yb:sudo chmod +rw rabbithutch}} to unlock the cage."
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"
    hints = [
        "{{rb:Use}} {{yb:sudo chmod +rw rabbithutch}} {{rb:to unlock the "
        "cage.}}"
    ]
    commands = [
        "sudo ./rabbithutch/fix-rabbit-script.sh"
    ]

    def next(self):
        Step64()


class Step64(StepTemplateSudo):
    story = [
        "The Rabbit jumps out of the rabbithutch.",
        "It blinks a couple of times.",
        "The red light has gone out of its eyes. It looks peaceful "
        "rubs its head affectionately on the Judoka.",
        "",
        "Judoka: {{Bb:Thank you for helping me and my friend. I don't "
        "we'll be causing anymore trouble here.}}",
        "{{Bb:Let's go Rabbit.}}"
    ]
    start_dir = "~/woods/thicket/.rabbithole/doorway"
    end_dir = "~/woods/thicket/.rabbithole/doorway"

    def next(self):
        time.sleep(3)
        self.exit()
