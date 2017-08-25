# challenge_10.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story
from linux_story.StepTemplate import StepTemplate
from linux_story.step_helper_functions import unblock_commands_with_cd_hint
from linux_story.story.terminals.terminal_cd import TerminalCd


class StepTemplateCd(StepTemplate):
    TerminalClass = TerminalCd


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateCd):
    story = [
        _("You're in your house. You appear to be alone."),
        _("Use {{yb:cat}} to {{lb:examine}} some of the objects around you.\n")
    ]
    allowed_commands = [
        "cat banana",
        "cat cake",
        "cat croissant",
        "cat grapes",
        "cat milk",
        "cat newspaper",
        "cat oven",
        "cat pie",
        "cat sandwich",
        "cat table"
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/my-house/kitchen"
    counter = 0
    deleted_items = ["~/my-house/kitchen/note"]
    file_list = [
        {"path": "~/town/.hidden-shelter/Eleanor"},
        {"path": "~/town/.hidden-shelter/Edward"},
        {"path": "~/town/.hidden-shelter/Edith"},
        {"path": "~/town/.hidden-shelter/apple"},
        {"path": "~/town/.hidden-shelter/dog"},
        {"path": "~/town/.hidden-shelter/basket/empty-bottle"},
        {"path": "~/town/.hidden-shelter/.tiny-chest/MV"},
    ]
    first_time = True

    def check_command(self, line):

        if line in self.allowed_commands:
            self.counter += 1
            self.allowed_commands.remove(line)
            hint = _("{{gb:Well done! Just look at one more item.}}")

        else:
            if self.first_time:
                hint = _("{{rb:Use}} {{yb:cat}} {{rb:to look at two of the " +\
                         "objects around you.}}")
            else:
                hint = _("{{rb:Use the command}} {{yb:%s}} {{rb:to progress.}}")\
                        % self.allowed_commands[0]

        level_up = (self.counter >= 2)

        if not level_up:
            self.send_hint(hint)
            self.first_time = False
        else:
            return level_up

    def next(self):
        return 10, 2


class Step2(StepTemplateCd):
    story = [
        _("There doesn't seem to be anything here but loads of food."),
        _("See if you can find something back in {{bb:town}}.\n"),
        _("First, use {{yb:cd ..}} to {{lb:leave}} the {{bb:kitchen}}.\n")
    ]
    start_dir = "~/my-house/kitchen"
    end_dir = "~/town"
    commands = [
        "cd ~/town",
        "cd ~/town/",
        "cd ..",
        "cd ../",
        "cd town",
        "cd town/",
        "cd ../..",
        "cd ../../",
        "cd"
    ]
    num_turns_in_home_dir = 0

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def check_command(self, line):
        if self.get_fake_path() == self.end_dir:
            return True

        hint = ""

        # decide command needed to get to next part of town
        if self.get_fake_path() == '~/my-house/kitchen' or self.get_fake_path() == '~/my-house':

            # If the last command the user used was to get here
            # then congratulate them
            if line == "cd .." or line == 'cd ../':
                hint = _("{{gb:Good work! Now replay the last command using " +\
                         "the}} {{ob:UP}} {{gb:arrow on your keyboard.}}")

            # Otherwise, give them a hint
            else:
                hint = _("{{rb:Use}} {{yb:cd ..}} {{rb:to make your way to town.}}")

        elif self.get_fake_path() == '~':
            # If they have only just got to the home directory,
            # then they used an appropriate command
            if self.num_turns_in_home_dir == 0:
                hint = _("{{gb:Cool! Now use}} {{yb:cd town}} {{gb:to head to town.}}")

            # Otherwise give them a hint
            else:
                hint = _("{{rb:Use}} {{yb:cd town}} {{rb:to go into town.}}")

            # So we can keep track of the number of turns they've been in the
            # home directory
            self.num_turns_in_home_dir += 1

        # print the hint
        self.send_hint(hint)

    def next(self):
        return 10, 3


class Step3(StepTemplateCd):
    story = [
        _("Use {{yb:ls}} to {{lb:look around}}.\n"),
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls"
    hints = [_("{{rb:Use}} {{yb:ls}} {{rb:to have a look around the town.}}")]

    def next(self):
        return 10, 4


class Step4(StepTemplateCd):
    story = [
        _("The place appears to be deserted."),
        _("However, you think you hear whispers."),
        # TODO make this writing small
        _("\n{{wb:?:}} {{Bn:\".....if they use}} {{yb:ls -a}}{{Bn:, they'll see us...\"}}"),
        _("{{wb:?:}} {{Bn:\"..Shhh! ...might hear....\"}}\n")
    ]
    start_dir = "~/town"
    end_dir = "~/town"
    commands = "ls -a"
    hints = [
        _("{{rb:You heard whispers referring to}} {{yb:ls -a}}" +\
        "{{rb:, try using it!}}"),
    ]

    def next(self):
        return 10, 5


class Step5(StepTemplateCd):
    story = [
        _("You see a {{bb:.hidden-shelter}} that you didn't notice before.\n"),
        _("{{gb:Something that starts with . is normally hidden from view.\n}}"),
        _("It sounds like the whispers are coming from there. Try going in.\n")
    ]
    start_dir = "~/town"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "cd .hidden-shelter",
        "cd .hidden-shelter/"
    ]
    hints = [
        _("{{rb:Try going inside the}} {{lb:.hidden-shelter}} {{rb:using }}" +\
        "{{yb:cd}}{{rb:.}}"),
        _("{{rb:Use the command}} {{yb:cd .hidden-shelter }}" +\
        "{{rb:to go inside.}}")
    ]

    def block_command(self, line):
        return unblock_commands_with_cd_hint(line, self.commands)

    def next(self):
        return 10, 6


class Step6(StepTemplateCd):
    story = [
        _("Is anyone there? Have a {{lb:look around}}.\n")
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town/.hidden-shelter"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to have a look around you.}}")
    ]

    def next(self):
        return 11, 1
