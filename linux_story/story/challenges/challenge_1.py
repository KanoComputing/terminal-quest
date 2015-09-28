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

from linux_story.story.terminals.terminal_ls import TerminalLs
from linux_story.story.challenges.challenge_2 import Step1 as NextChallengeStep


class StepLs(TerminalLs):
    challenge_number = 1


class Step1(StepLs):
    story = [
        "{{wb:Sveglia}} : \"Beep beep beep! Beep beep beep!\"",
        "{{wb:Radio}} : {{Bb:\"Buongiorno, questo è il notiziario delle 9.\"",
        "\"Strane voci di primo mattino a Strada in Chianti. "
        "Si chiacchera di gente sparita e case danneggiate"
        " in paese, a breve trasmetteremo nuove notizie.\"",
        "\"Il sindaco ha indetto una riunione d'emergenza,"
        " vi riferiremo appena avrà avuto luogo...\"}}\n",
        "È l'ora di svegliarsi dormiglione!",
        "\n{{gb:Primo comando:}} Scrivi {{yb:ls}} e premi {{wb:Invio}} per "
        "{{lb:guardarti attorno}}.\n"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"
    commands = "ls"
    hints = [
        "{{rb:Scrivi}} {{yb:ls}} {{rb:e premi Invio per guardarti intorno "
        "in camera tua.}}"
    ]

    last_step = True

    def next(self):
        NextChallengeStep(self.xp)
