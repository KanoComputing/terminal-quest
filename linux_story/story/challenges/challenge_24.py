#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story


from linux_story.story.terminals.terminal_eleanor import TerminalMkdirEleanor
from linux_story.story.challenges.challenge_25 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateMkdir(TerminalMkdirEleanor):
    challenge_number = 24


class Step1(StepTemplateMkdir):
    story = [
        "Ti sei incamminato lungo questa stradina, insieme a Eleonora "
        "che ti saltella accanto, quando arrivate in uno spazio aperto "
        "a {{bb:est}} del paese.",
        "\n{{lb:Guarda attorno.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est"
    hints = [
        "{{rb:Guarda intorno con}} {{yb:ls}}{{rb:.}}"
    ]
    deleted_items = ["~/paese/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est"
        }
    }

    eleanors_speech = (
        "Eleonora: {{Bb:Non riesco a vedere i miei genitori da nessuna parte... "
        "ma c'è uno strano edificio laggiù.}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        "Vedi un {{bb:negozio di capanni}}, una {{bb:biblioteca}} e un {{bb:ristorante}}.",
        "\nEleonora: {{Bb:Guarda buffo, un negozio di capanni!}}",
        "{{Bb:Andiamo}} {{lb:dentro}}{{Bb:!}}"
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est/negozio-di-capanni"
    hints = [
        "{{rb:Usa}} {{yb:cd negozio-di-capanni/}} {{rb:per andare nel negozio di capanni.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Pensi che vendano caramelle?}}"
    )

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


# Duplicate of Step1, except that self.next is changed
class Step3(StepTemplateMkdir):
    # Have a sign with "the-best-shed-maker-in-paese"

    story = [
        "Entrate insieme lentamente nel negozio.",
        "È buio e polveroso qui dentro.",
        "Eleonora sta per starnutire.",
        "\n{{lb:Guarda intorno.}}"
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"
    hints = [
        "{{rb:Guarda intorno con}} {{yb:ls}}{{rb:.}}"
    ]
    commands = [
        "ls",
        "ls -a"
    ]
    deleted_items = ["~/paese/est/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est/negozio-di-capanni"
        }
    }
    eleanors_speech = (
        "Eleonora: {{Bb:Eh..eh...etciuu!! Mamma com'è polveroso qui dentro!}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):

    story = [
        "C'è un uomo che si chiama Bernardo, una porta e "
        "un paio di attrezzi.",
        "\nI nomi degli attrezzi sono scritti in {{gb:verde}} nel Terminale.",
        "\n{{lb:Ascolta}} cosa dice {{lb:Bernardo}}."
    ]

    start_dir = "~/paese/est/negozio-di-capanni"
    end_dir = "~/paese/est/negozio-di-capanni"

    hints = [
        "{{rb:Usa}} {{yb:cat Bernardo}} {{rb:per ascoltarlo.}}"
    ]

    commands = [
        "cat Bernardo"
    ]
    eleanors_speech = (
        #arf This can't be translated in Italian    
        #arf "Eleonora: {{Bb:My}} {{lb:cat}} {{Bb:used to be a great "
        #arf "listener, I'd tell her everything.}}"
        "Eleonora: {{Bb:Sentiamo...}}"
    )

    last_step = True

    def next(self):
        NextStep(self.xp)
