# challenge_2.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.StepTemplate import StepTemplate
from kano_profile.apps import save_app_state_variable
from linux_story.helper_functions import wrap_in_box
from linux_story.story.terminals.terminal_cat import TerminalCat


class StepCat(StepTemplate):
    TerminalClass = TerminalCat


# ----------------------------------------------------------------------------------------


class Step1(StepCat):
    story = [
        _("Awesome, now you can see the objects around you."),
        _("There's your {{bb:bed}}, an {{bb:alarm}}... "),
        _("Euuughh...turn that {{bb:alarm}} off! \n"),
    ]

    story += wrap_in_box([
        _("{{gb:New Power}}: to {{lb:examine}} objects, type"),
        _("{{yb:cat}} and the object name."),
    ])

    story += [
        _("Use {{yb:cat alarm}} to {{lb:examine}} the {{bb:alarm}}.")
    ]

    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat alarm"
    highlighted_commands = ['cat']
    hints = [_("{{rb:Type}} {{yb:cat alarm}} {{rb:to investigate the alarm.}}")]

    def next(self):
        return 2, 2


class Step2(StepCat):
    story = [
        _("Ok - it's switched off. Better get dressed...\n"),

        _("Type {{yb:ls wardrobe/}} to {{lb:look inside}} your {{bb:wardrobe}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = ["ls wardrobe", "ls wardrobe/"]
    hints = [
        _("{{rb:Type}} {{yb:ls wardrobe/}} {{rb:to look for something to wear.}}")
    ]

    def next(self):
        return 2, 3


class Step3(StepCat):
    story = [
        _("Check out that {{bb:t-shirt}}!\n"),
        _("{{lb:Examine}} the {{bb:t-shirt}} with {{yb:cat wardrobe/t-shirt}} to see how it looks.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat wardrobe/t-shirt"
    hints = [
        _("{{rb:Type}} {{yb:cat wardrobe/t-shirt}} {{rb:to investigate how it looks.}}")
    ]

    def next(self):
        return 2, 4


class Step4(StepCat):
    story = [
        _("Looking good! Put that on and look for something else.\n"),
        _("{{lb:Examine}} the {{bb:skirt}} or the {{bb:trousers}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/skirt",
        "cat wardrobe/trousers"
    ]
    hints = [
        _("{{rb:Type}} {{yb:cat wardrobe/trousers}} {{rb:or}} {{yb:cat wardrobe/skirt}} {{rb:to dress yourself.}}")
    ]
    checked_outside_wardrobe = False

    def check_command(self, line):
        if line == self.commands[0]:
            save_app_state_variable('linux-story', 'outfit', 'skirt')
        elif line == self.commands[1]:
            save_app_state_variable('linux-story', 'outfit', 'trousers')
        elif not self.checked_outside_wardrobe and (line == "cat trousers" or line == "cat skirt"):
            self.send_hint(_("\n{{rb:You need to look in your}} {{bb:wardrobe}} {{rb:for that item.}}"))
            self.checked_outside_wardrobe = True

        return StepCat.check_command(self, line)

    def next(self):
        return 2, 5


class Step5(StepCat):
    story = [
        _("Awesome, you're nearly dressed to quest.\n"),
        _("Finally, check out that {{bb:cap}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = [
        "cat wardrobe/cap"
    ]
    hints = [
        _("{{rb:Type}} {{yb:cat wardrobe/cap}} {{rb:to}} {{lb:examine}} {{rb:the cap.}}")
    ]

    last_step = True

    def next(self):
        return 3, 1
