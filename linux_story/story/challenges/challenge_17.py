#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_mv import TerminalMv
from linux_story.story.terminals.terminal_echo import TerminalEcho
from linux_story.story.challenges.challenge_18 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands
from kano_profile.apps import (
    save_app_state_variable, load_app_state_variable
)


# This is for the challenges that only need ls
class StepTemplateMv(TerminalMv):
    challenge_number = 17


# This is for that challenges that need echo
class StepTemplateEcho(TerminalEcho):
    challenge_number = 17


class Step1(StepTemplateMv):
    story = [
        "Sei nella tua camera, ritto davanti allo {{bb:.scrigno}} "
        "che contiene i comandi che hai imparato fin'ora.",
        "Magari c'è qualcos'altro nascosto in casa?",
        "{{lb:Cerca}} nell'ingresso {{lb:da dove sei entrato}}.  Ricorda, "
        "il luogo da dove sei venuto è {{lb:..}} or {{lb:../}}"
    ]
    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-mia"
    hints = [
        "{{rb:Guarda nel luogo da dove sei venuto con}} {{yb:ls ../}}"
    ]
    commands = [
        "ls ..",
        "ls ../"
    ]

    def next(self):
        Step2()


class Step2(StepTemplateMv):
    story = [
        "Ci sono le porte per andare in {{bb:giardino}}, {{bb:cucina}}, "
        "{{bb:camera-mia}} e {{bb:camera-genitori}}.",
        "Non abbiamo controllato perbene la camera dei genitori ancora.",
        "{{lb:Vai nella camera-genitori}}."
    ]

    start_dir = "~/casa-mia/camera-mia"
    end_dir = "~/casa-mia/camera-genitori"

    # This is for the people who are continuing to play from the
    # beginning.
    # At the start, add the fattoria directory to the file system
    # Also add the map and journal in your Mum's room
    story_dict = {
        "Gelsomino, Trogolo, Violetta, Romina": {
            "path": "~/fattoria/fienile"
        },
        "MKDIR, chiave-inglese, martello, sega, metro": {
            "path": "~/fattoria/capanno-degli-attrezzi"
        },
        "casa-della-fattoria": {
            "path": "~/fattoria",
            "directory": True
        },
        # this should be added earlier on, but for people who have updated,
        # we should figure out how to give them the correct file system
        "ECHO, diario-della-mamma, mappa": {
            "path": "~/casa-mia/camera-genitori/.cassaforte"
        }
    }

    path_hints = {
        "~/casa-mia/camera-mia": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/casa-mia": {
            "not_blocked": "\n{{gb:Bene! Ora vai nella}} {{lb:camera-genitori}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd camera-genitori/}} {{rb:per entrare.}}"
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
        Step3()


class Step3(StepTemplateMv):
    story = [
        "Guarda intorno {{lb:attentamente}}."
    ]
    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~/casa-mia/camera-genitori"

    hints = [
        "{{rb:Usa il comando}} {{yb:ls -a}} {{rb:per guardare bene.}}"
    ]
    commands = [
        "ls -a",
        "ls -a .",
        "ls -a ./"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step4()


class Step4(StepTemplateMv):
    story = [
        "C'è una {{lb:.cassaforte}}!",
        "Magari c'è qualcosa di utile dentro. {{lb:Guarda dentro}} la "
        "{{lb:.cassaforte}}."
    ]

    commands = [
        "ls .cassaforte",
        "ls .cassaforte/",
        "ls -a .cassaforte",
        "ls -a .cassaforte/"
    ]
    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~/casa-mia/camera-genitori"
    hints = [
        "{{rb:Guarda la}} {{lb:.cassaforte}} {{rb:usando}} {{lb:ls}}{{rb:.}}",
        "{{rb:Usa}} {{yb:ls .cassaforte}} {{rb:per guardare la .cassaforte.}}"
    ]

    def next(self):
        Step5()


# This class is here so if the user checks the diary,
# they get told off
class CheckDiaryStep(StepTemplateMv):
    def __init__(self, check_diary=0):
        self.check_diary = check_diary
        StepTemplateMv.__init__(self)

    def check_command(self):
        checked_diary = load_app_state_variable(
            "linux-story", "checked_mums_diary"
        )
        # Check to see if the kid reads his/her Mum's journal
        if self.last_user_input == 'cat .cassaforte/diario-della-mamma' and \
                not checked_diary:
            self.send_hint(
                "\n{{rb:Hai letto il diario della mamma!}} "
                "{{ob:Hai fatto rumore, ti hanno sentito.}}"
            )
            save_app_state_variable("linux-story", "checked_mums_diary", True)
            return False

        return StepTemplateMv.check_command(self)


class Step5(CheckDiaryStep):
    story = [
        "Allora, hai trovato il diario della mamma?",
        "Forse non lo dovresti leggere...",
        "Che altro c'è qui?  {{lb:Vediamo}} questa {{lb:mappa}}."
    ]
    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~/casa-mia/camera-genitori"
    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:per leggere la}} {{lb:mappa}}{{rb:.}}",
        "{{rb:Usa}} {{yb:cat .cassaforte/map}} {{rb:per leggere la mappa.}}"
    ]

    commands = "cat .cassaforte/mappa"

    def next(self):
        Step6(self.check_diary)


class Step6(CheckDiaryStep):
    story = [
        "Allora c'è una fattoria da queste parti?",
        "Sembrerebbe non essere lontana da casa nostra, giusto fuori dalla via ventosa...",
        "Cos'è questo foglietto {{lb:ECHO}}? {{lb:Controlla}} il foglietto ECHO."
    ]

    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~/casa-mia/camera-genitori"
    commands = "cat .cassaforte/ECHO"
    hints = [
        "{{rb:Usa il comando}} {{lb:cat}} {{rb:per leggere il foglietto}} {{lb:ECHO}}"
        "{{rb:.}}",
        "{{rb:Usa}} {{yb:cat .cassaforte/ECHO}} {{rb:per leggere il foglietto.}}"
    ]

    def next(self):
        Step7()


class Step7(StepTemplateEcho):
    story = [
        "Insomma iil foglietto dice {{lb:echo ciao - ti farà dire ciao}}",
        "Proviamo. "
        "Usa il comando {{yb:echo ciao}}"
    ]
    hints = [
        "{{rb:Usa il comando}} {{yb:echo ciao}}"
    ]
    commands = [
        "echo ciao",
        "echo CIAO",
        "echo Ciao"
    ]
    start_dir = "~/casa-mia/camera-genitori"
    end_dir = "~/casa-mia/camera-genitori"
    last_step = True

    def next(self):
        NextStep(self.xp)
