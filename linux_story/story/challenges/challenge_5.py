# challenge_5.py
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
from linux_story.story.challenges.challenge_6 import Step1 as NextChallengeStep
from linux_story.step_helper_functions import unblock_commands_with_cd_hint


class StepTemplateCd(TerminalCd):
    challenge_number = 5


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("{{wb:Mum:}} {{Bb:\"Hi sleepyhead, breakfast is nearly ready. Can you go and grab your Dad? I think he's in the}} {{bb:garden}}{{Bb:.\"}}\n"),
        _("Let's look for your {{bb:Dad}} in the {{bb:garden}}."),
        _("First we need to {{lb:leave}} the {{bb:kitchen}} using {{yb:cd ..}}\n")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house"
    commands = ["cd ..", "cd ../"]
    hints = _("{{rb:To leave the kitchen, type}} {{yb:cd ..}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step2()


class Step2(StepTemplateCd):
    story = [
        _("You are back in the main hall of your house.\n"),
        _("Can you see your {{bb:garden}}? Have a {{lb:look around}} you.\n")
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house"
    commands = "ls"
    hints = _("{{rb:Type}} {{yb:ls}} {{rb:to look around you.}}")

    def next(self):
        Step3()


class Step3(StepTemplateCd):
    story = [
        _("You see doors to the {{bb:garden}}, {{bb:kitchen}}, {{bb:my-room}} and {{bb:parents-room}}."),
        _("{{lb:Go}} into your {{bb:garden}}.\n")
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house/garden"
    commands = ["cd garden", "cd garden/"]
    hints = _("{{rb:Type}} {{yb:cd garden}} {{rb:to go into the garden.}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateCd):
    story = [
        _("Use {{yb:ls}} to {{lb:look}} in the {{bb:garden}} for your {{bb:Dad}}.\n")
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house/garden"
    commands = "ls"
    hints = _("{{rb:To look for your Dad, type}} {{yb:ls}} {{rb:and press {{ob:Enter}}{{rb:.}}")

    def next(self):
        Step5()


class Step5(StepTemplateCd):
    story = [
        _("The {{bb:garden}} looks beautiful at this time of year."),
        _("Hmmm...but you can't see him anywhere."),
        _("Maybe he's in the {{bb:greenhouse}}."),
        _("\n{{lb:Go}} inside the {{bb:greenhouse}}.\n")
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house/garden/greenhouse"
    commands = ["cd greenhouse", "cd greenhouse/"]
    hints = _("{{rb:To go to the greenhouse, type}} {{yb:cd greenhouse}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step6()


class Step6(StepTemplateCd):
    story = [
        _("Is he here? {{lb:Look around}} with {{yb:ls}} to find out.\n")
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden/greenhouse"
    commands = "ls"
    hints = _("{{rb:Type}} {{yb:ls}} {{rb:to look for your Dad.}}")

    def next(self):
        Step7()


class Step7(StepTemplateCd):
    story = [
        _("Your {{bb:Dad}} has been busy, there are loads of vegetables here."),
        _("Hmmmm. He's not here. But there is something odd.\n"),
        _("You see a {{bb:note}} on the ground. Use {{yb:cat note}} to {{lb:read}} what it says.\n")
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden/greenhouse"
    commands = "cat note"
    hints = _("{{rb:Type}} {{yb:cat note}} {{rb:to see what the note says!}}")

    def next(self):
        Step8()


class Step8(StepTemplateCd):
    story = [
        _("Going back is super easy. Just type {{yb:cd ..}} to go back the way you came.\n")
    ]
    start_dir = "~/my-house/garden/greenhouse"
    end_dir = "~/my-house/garden"
    commands = ["cd ..", "cd ../"]
    hints = _("{{rb:Type}} {{yb:cd ..}} {{rb:to go back to the garden.}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step9()


class Step9(StepTemplateCd):
    story = [
        _("You're back in the garden. Use {{yb:cd ..}} again to {{lb:go back}} to the house.\n"),
        _("{{gb:Top tip: Press the}} {{ob:UP}} {{gb:arrow key to replay your previous command.}}\n")
    ]
    start_dir = "~/my-house/garden"
    end_dir = "~/my-house"
    commands = ["cd ..", "cd ../"]
    hints = _("{{rb:Type}} {{yb:cd ..}} {{rb:to go back to the house.}}")

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step10()


class Step10(StepTemplateCd):
    story = [
        _("Now {{lb:go}} back into the {{bb:kitchen}} and see {{bb:Mum}}.\n")
    ]
    start_dir = "~/my-house"
    end_dir = "~/my-house/kitchen"
    commands = ["cd kitchen", "cd kitchen/"]
    hints = _("{{rb:Type}} {{yb:cd kitchen}} {{rb:to go back to the kitchen.}}")

    last_step = True

    def block_command(self):
        return unblock_commands_with_cd_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        NextChallengeStep(self.xp)
