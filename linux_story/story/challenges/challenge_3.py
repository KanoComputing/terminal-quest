#!/usr/bin/env python
# coding: utf-8

#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

# from linux_story.Step import Step
from linux_story.story.terminals.terminal_cat import TerminalCat
from linux_story.story.challenges.challenge_4 import Step1 as NextChallengeStep


class StepTemplateCat(TerminalCat):
    challenge_number = 3


class Step1(StepTemplateCat):
    story = [
#        "Love it! Put it on quickly.",
        "Mi piace! Mettilo di corsa.",
#        "There's loads more interesting stuff in your room.",
        "C'è un sacco di roba interessante in camera tua.",
#        "Let's {{lb:look}} in your {{lb:shelves}} using {{lb:ls}}.\n"
        "{{lb:Guarda}} nei tuoi {{lb:scaffali}} using {{lb:ls}}.\n"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"
#    commands = ["ls shelves", "ls shelves/"]
    commands = ["ls scaffali", "ls scaffali/"]
#    hints = "{{rb:Type}} {{yb:ls shelves/}} {{rb:to look at your books.}}"
    hints = "{{rb:Scrivi}} {{yb:ls scaffali/}} {{rb:per guardare i tuoi libri.}}"

    def next(self):
        Step2()


class Step2(StepTemplateCat):
    story = [
#        "Did you know you can use the TAB key to speed up your typing?",
        "Lo sapevi che puoi usare il tasto TAB per scrivere i comandi più alla svelta?",
#        "Try it by checking out that comic book. {{lb:Examine}} it with "
        "Prova prendendo quel fumetto. {{lb:Guardalo}} con "
#        "{{yb:cat shelves/comic-book}}",
        "{{yb:cat scaffali/fumetto}}",
#        "Press the TAB key before you've finished typing!\n"
        "Premi il tasto TAB prima di avere finito di scrivere il comando!\n"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"
#    commands = "cat shelves/comic-book"
    commands = "cat scaffali/fumetto"
#    hints = "{{rb:Type}} {{yb:cat shelves/comic-book}} {{rb:to read the comic.}}"
    hints = "{{rb:Scrivi}} {{yb:cat scaffali/fumetto}} {{rb:per leggerlo.}}"

    def next(self):
        Step3()


class Step3(StepTemplateCat):
    story = [
#        "Why is it covered in pawprints?",
        "O perché c'è un'impronta sopra?",
#        "Hang on, can you see that? There's a {{lb:note}} amongst your books.",
        "Aspetta? C'è un {{lb:foglietto}} fra i tuoi libri.",
#        "{{lb:Read}} the note using {{lb:cat}}.\n"
        "{{lb:Leggilo}} usando il comando {{lb:cat}}.\n"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"
#    commands = "cat shelves/note"
    commands = "cat scaffali/foglietto"
#    hints = "{{rb:Type}} {{yb:cat shelves/note}} {{rb:to read the note.}}"
    hints = "{{rb:Scrivi}} {{yb:cat scaffali/foglietto}} {{rb:per leggerlo.}}"

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
