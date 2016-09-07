# challenge_20.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_21 import Step1 as NextStep
from linux_story.step_helper_functions import \
    unblock_commands_with_mkdir_hint, unblock_cd_commands
from linux_story.helper_functions import wrap_in_box


class StepTemplateEcho(TerminalEcho):
    challenge_number = 20


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 20


# ----------------------------------------------------------------------------------------


class Step1(StepTemplateEcho):
    print_text = [
        _("{{yb:\"Some people survived by going into hiding.\"}}")
    ]
    story = [
        _("Ruth: {{Bb:\"Oh! That reminds me, my husband used " +\
        "to build special shelters to store crops in over winter. " +\
        "I think he used a specific tool. " +\
        "We should take a look in his toolshed to see if we can find it.\"}}"),
        _("\nUse the {{lb:cd}} command to go into the {{bb:toolshed}}.\n")
    ]

    start_dir = "~/farm/barn"
    end_dir = "~/farm/toolshed"
    hints = [
        _("{{rb:Go to the toolshed in one step" +\
        " using}} {{yb:cd ../toolshed}}")
    ]

    path_hints = {
        "~/farm/barn": {
            "blocked": _("\n{{rb:Use}} {{yb:cd ..}} {{rb:to go back.}}")
        },
        "~/farm": {
            "not_blocked": _("\n{{gb:You walk outside. Now go into the}} {{bb:toolshed}}{{gb:.}}"),
            "blocked": _("\n{{rb:Use}} {{yb:cd toolshed}} {{rb:to go in the toolshed.}}")
        }
    }

    def check_command(self):
        if self.current_path == self.end_dir:
            return True
        elif "cd" in self.last_user_input and not self.get_command_blocked():
            hint = self.path_hints[self.current_path]["not_blocked"]
        else:
            hint = self.path_hints[self.current_path]["blocked"]

        self.send_text(hint)

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step2()


class Step2(StepTemplateEcho):
    story = [
        _("{{bb:Ruth}} follows you into the {{bb:toolshed}}. It's a very large " +\
        "space with tools lining the walls.\n"),
        _("Ruth: {{Bb:\"Let's}} {{lb:look around}} {{Bb:for " +\
        "anything that could be useful.\"}}\n")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    hints = [
        _("{{rb:Use}} {{yb:ls}} {{rb:to look around.}}")
    ]
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./",
        "ls -a .",
        "ls -a ./"
    ]
    # Move Ruth into toolshed
    story_dict = {
        "Ruth": {
            "path": "~/farm/toolshed"
        }
    }
    deleted_items = ["~/farm/barn/Ruth"]

    def next(self):
        Step3()


class Step3(StepTemplateEcho):
    story = [
        _("Ruth: {{Bb:\"Ah, look! There are some instructions " +\
        "under}} {{bb:MKDIR}}{{Bb:.\"}}"),
        _("{{Bb:\"What does it say?\"}}"),
        _("\n{{lb:Examine}} the {{bb:MKDIR}} instructions.")
    ]
    hints = [
        _("Ruth: {{Bb:\"...you are able to read, yes? You use}} {{yb:cat}} " +\
        "{{Bb:to read things.\"}}"),
        _("Ruth: {{Bb:\"What do you kids learn in schools nowadays...\"" +\
        "\n\"Just use}} {{yb:cat MKDIR}} {{Bb:to read the paper.\"}}"),
        _("{{rb:Use}} {{yb:cat MKDIR}} {{rb:to read it.}}")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = "cat MKDIR"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        _("Ruth: {{Bb:\"This says you can make something using something " +\
        "called}} {{yb:mkdir}}{{Bb:?\"}}"),
        _("\nTry making an igloo using {{yb:mkdir igloo}}\n "),
    ]

    story += wrap_in_box([
        _("{{gb:New Spell}}: {{yb:mkdir}} followed by a word"),
        _("lets you {{lb:create}} a shelter"),
    ])

    hints = [
        _("{{rb:Create an igloo structure by using}} {{yb:mkdir igloo}}\n")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "mkdir igloo"
    ]
    highlighted_commands = ['mkdir']

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def check_command(self):
        if self.last_user_input == "cat MKDIR":
            self.send_hint(_("\n{{gb:Well done for checking the page again!}}"))
            return False

        return StepTemplateMkdir.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        _("Now have a {{lb:look around}} and see what's changed.")
    ]
    start_dir = "~/farm/toolshed"
    end_dir = "~/farm/toolshed"
    commands = [
        "ls",
        "ls -a",
        "ls .",
        "ls ./"
    ]
    hints = [
        _("{{rb:Look around using}} {{yb:ls}}{{rb:.}}")
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
