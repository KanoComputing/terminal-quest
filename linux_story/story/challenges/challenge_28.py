#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.story.terminals.terminal_bernard import TerminalNanoBernard
from linux_story.story.challenges.challenge_29 import Step1 as NextStep
from linux_story.step_helper_functions import unblock_cd_commands


class StepTemplateNano(TerminalNanoBernard):
    challenge_number = 28


class Step1(StepTemplateNano):
    story = [
        "Siamo di nuovo in paese. Eleonora è sollevata di essere "
        "uscita.",
        "Dove si potrà essere nascosta la bibliotecaria?",
        "{{lb:Guarda intorno}} per decidere dove andare."
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est"

    hints = [
        "{{rb:Usa}} {{yb:ls}} {{rb:per guardare intorno.}}"
    ]

    deleted_items = ["~/paese/est/negozio-di-capanni/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est"
        }
    }
    commands = [
        "ls",
        "ls -a"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Ho fame. Vedi un posto dove si possa mangiare?}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    story = [
        "Non abbiamo controllato il ristorante ancora.",
        "Sì, {{lb:andiamo}} nel {{lb:ristorante}}."
    ]

    start_dir = "~/paese/est"
    end_dir = "~/paese/est/ristorante"

    hints = [
        "{{rb:Usa}} {{yb:cd ristorante}} {{rb:per andare nel ristorante.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Ooh, pensi che abbiano dei panini?}}"
    )

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    story = [
        "Tu e Eleonora entrate nel ristorante.",
        "Guarda intorno {{lb:attentamente}}."
    ]

    start_dir = "~/paese/est/ristorante"
    end_dir = "~/paese/est/ristorante"

    hints = [
        "Eleonora: {{Bb:Ti ricordi come mi avevi trovato?"
        " Avevi usato}} {{yb:ls -a}} {{Bb:giusto?}}"
    ]

    commands = [
        "ls -a"
    ]

    deleted_items = ["~/paese/est/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est/ristorante"
        }
    }

    eleanors_speech = (
        "Eleonora: {{Bb:Sembra tutto vuoto qui...}}"
    )

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    story = [
        "La vedi la {{bb:.cantina}}?",
        "{{lb:Andiamo}} nella {{lb:.cantina}}."
    ]

    start_dir = "~/paese/est/ristorante"
    end_dir = "~/paese/est/ristorante/.cantina"

    hints = [
        "{{rb:Vai nella cantina dei vini usando}} {{yb:cd .cantina}}{{rb:.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Ho paura...mi dai la mano?}}"
    )

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step5()


class Step5(StepTemplateNano):
    story = [
        "Eleonora afferra la tua mano, e scendete insieme nella .cantina.",
        "{{lb:Guarda attorno.}}"
    ]

    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"

    hints = [
        "{{rb:Guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]

    deleted_items = ["~/paese/est/ristorante/Eleonora"]
    story_dict = {
        "Eleonora": {
            "path": "~/paese/est/ristorante/.cantina"
        }
    }
    commands = [
        "ls",
        "ls -a"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:...c'è qualcuno qui?}}"
    )

    def next(self):
        Step6()


class Step6(StepTemplateNano):
    story = [
        "C'è una donna, {{lb:Clara}}, in cantina.",
        "{{lb:Ascolta}} quello che dice."
    ]

    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"

    hints = [
        "{{rb:Usa}} {{lb:cat}} {{rb:per ascoltare cosa dice.}}",
        "{{rb:Usa}} {{yb:cat Clara}} {{rb:per ascoltare Clara.}}"
    ]

    commands = [
        "cat Clara"
    ]
    eleanors_speech = (
        "Eleonora: {{Bb:...oh! Ma io riconosco questa donna!}}"
    )

    last_step = True

    def next(self):
        NextStep(self.xp)
