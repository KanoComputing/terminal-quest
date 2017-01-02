# challenge_3.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.IStep import IStep
from linux_story.story.new_terminals.terminal_cat import TerminalCat


class StepTemplateCat(IStep):
    TerminalClass = TerminalCat


class Step1(StepTemplateCat):
    story = [
        _("Love it! Put it on quickly."),
        _("There's loads more interesting stuff in your room.\n"),
        _("Let's {{lb:look}} in your {{bb:shelves}} using {{yb:ls}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = ["ls shelves", "ls shelves/"]
    hints = [_("{{rb:Type}} {{yb:ls shelves/}} {{rb:to look at your books.}}")]

    def next(self):
        return 3, 2


class Step2(StepTemplateCat):
    story = [
        _("Did you know you can use the {{ob:TAB}} key to speed up your typing?"),
        _("Try it by checking out that {{bb:comic book}}.\n"),
        _("{{lb:Examine}} it with {{yb:cat shelves/comic-book}}\n"),
        _("Press the {{ob:TAB}} key before you've finished typing!\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat shelves/comic-book"
    hints = [_("{{rb:Type}} {{yb:cat shelves/comic-book}} {{rb:to read the comic.}}")]

    def next(self):
        return 3, 3


class Step3(StepTemplateCat):
    story = [
        _("Why is it covered in pawprints?"),
        _("Hang on, can you see that? There's a {{bb:note}} amongst your books.\n"),
        _("{{lb:Read}} the {{bb:note}} using {{yb:cat}}.\n")
    ]
    start_dir = "~/my-house/my-room"
    end_dir = "~/my-house/my-room"
    commands = "cat shelves/note"
    hints = [_("{{rb:Type}} {{yb:cat shelves/note}} {{rb:to read the note.}}")]

    def next(self):
        return 4, 1
