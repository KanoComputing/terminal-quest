#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_bernard import TerminalNanoBernard
from linux_story.story.challenges.challenge_30 import Step1 as NextStep
from linux_story.helper_functions import play_sound, record_user_interaction


# Can't get all the information with this system unless you are interested.
story_replies = {
    "echo 1": [
        {
            "user": "Perché la sezione privata della biblioteca è chiusa?",
            "clara": (
                "Clara: {{Bb:Contiene delle informazioni pericolose."

                "\n...Mi dispiace, non dovrei dire altro. Il direttore "
                "era molto preoccupato che qualcuno potesse entrare. "
                "Lui è l'unico che sa chiudere e aprire.}}"
            )
        },
        {
            "user": "E come ha fatto a chiuderla?",
            "clara": (
                "Clara: {{Bb:Non lo so, non avevo un grado sufficiente "
                "perché mi venisse detto.}}"

                "\n{{Bb:Penso che lui l'abbia imparato dallo}} "
                "{{lb:spadaccino mascherato}} "
                "{{Bb:che sta fuori del paese.}}"
            )
        },
        {
            "user": "Dove sarebbe questo spadaccino mascherato?",
            "clara": (
                "Clara: {{Bb:Ha detto che lo}} "
                "{{lb: spadaccino mascherato}} {{Bb:vive nel bosco.}}"

                "\n{{Bb:Presumo che intendesse il bosco giusto "
                "intorno alla}} "
                "{{lb:strada ventosa}}{{Bb:? Quello "
                "vicino alla fattoria e quella casa isolata buffa "
                "fuori del paese.}}"
            )
        }
    ],

    "echo 2": [
        {
            "user": "Ma perché ti nascondi qui?",
            "clara": (
                "Clara: {{Bb:Ho sentito suonare la campanella, e ho visto "
                "sparire il direttore davanti a me. Mi sono "
                "così spaventata che sono scappata e ho trovato "
                "questa }} {{bb:.cantina}}"
                "{{Bb:.}}"
            )
        },
        {
            "user": "Hai dei parenti in paese?",
            "clara": (
                "Clara: {{Bb:Ho due figli, un}} "
                "{{lb:bambino}} {{Bb:e una}} "
                "{{lb:bambina}}{{Bb:. Spero che stiano bene.}}"
            )
        },
        {
            "user": "Perché la biblioteca è così vuota?",
            "clara": (
                "Clara: {{Bb:Avremmo introdotto delle multe per i "
                "ritardi, diverso tempo fa...}}"
            )
        }
    ],

    "echo 3": [
        {
            "user": "Conosci altra gente in paese?",
            "clara": (
                "Clara: {{Bb:C'è un uomo , del quale non mi fido, "
                "che gestisce il}} {{bb:negozio di capanni}}"
                "{{Bb:. Mi sembra che si chiami Bernardo.}}"
            )
        },
        {
            "user": "Perché non ti piace Bernardo?",
            "clara": (
                "Clara: {{Bb:Fabbrica degli attrezzi molto semplici "
                " e poi se li fa pagare un occhio.}}"
                "\n{{Bb:Il suo babbo era un uomo molto intelligente "
                "che passava un sacco di tempo in biblioteca a "
                "imparare i comandi. In questo modo è diventato "
                "un ottimo uomo d'affari.}}"
            )
        },
        {
            "user": "Che è successo poi al babbo di Bernardo?",
            "clara": (
                "Clara: {{Bb:Nessuno lo sa di preciso, un bel "
                "giorno è semplicemente sparito. "
                "S'è pensato che fosse morto. Lo vidi uscire di "
                "biblioteca il giorno che poi sparì. Mi ricordo "
                "che uscì in fretta e sembrava assolutamente "
                "terrorizzato.}}"
            )
        }
    ]
}


# Generate the story from the step number
def create_story(step):
    print_text = ""

    if step > 1:
        print_text = "{{yb:" + story_replies["echo 1"][step - 2]["user"] + "}}"

    story = [
        story_replies["echo 1"][step - 2]["clara"],
        "\n{{yb:1: " + story_replies["echo 1"][step - 1]["user"] + "}}",
        "{{yb:2: " + story_replies["echo 2"][0]["user"] + "}}",
        "{{yb:3: " + story_replies["echo 3"][0]["user"] + "}}"
    ]

    return (print_text, story)


# Want to eliminate the story that the user has already seen
def pop_story(user_input):
    # if the user_input is echo 1, echo 2 or echo 3
    if user_input in story_replies:
        reply = story_replies[user_input][0]
        story_replies[user_input].remove(reply)
        return reply


class StepNano(TerminalNanoBernard):
    challenge_number = 29


class StepNanoStory(StepNano):
    commands = [
        "echo 1"
    ]

    start_dir = "~/paese/est/ristorante/.cantina"
    end_dir = "~/paese/est/ristorante/.cantina"
    hints = [
        "{{rb:Parla a Clara usando}} {{yb:echo 1}}{{rb:,}} "
        "{{yb:echo 2}} {{rb:o}} {{yb:echo 3}}{{rb:.}}"
    ]

    def __init__(self, xp="", step_number=None):
        self.echo_hit = {
            "echo 2": True,
            "echo 3": True
        }

        if step_number:
            self.print_text = [create_story(step_number)[0]]
            self.story = create_story(step_number)[1]

        StepNano.__init__(self, "")

    def check_command(self):

        # If self.last_user_input equal to "echo 1" or "echo 3"
        if self.last_user_input in story_replies:

            if self.last_user_input == "echo 1":
                return True

            else:
                if self.echo_hit[self.last_user_input]:
                    self.echo_hit[self.last_user_input] = False
                    reply = pop_story(self.last_user_input)["clara"]
                    self.send_text("\n\n" + reply)

                    # Record that the user got optional info
                    # Replace spaces with underscores
                    user_input = "_".join(self.last_user_input.split(" "))
                    state_name = "clara_{}".format(user_input)
                    record_user_interaction(self, state_name)
                else:
                    self.send_text(
                        "\n{{rb:Questo l'hai già chiesto a Clara. "
                        "Domandale qualcos'altro.}}"
                    )

        else:
            return TerminalNanoBernard.check_command(self)


class Step1(StepNanoStory):
    story = [
        "Clara: {{Bb:Cosa? Chi sei?}}",

        "\nEleonora: {{Bb:Ciao! Sono Eleonora, e questo è}} {{gb:" +
        os.environ["LOGNAME"] + "}}{{Bb:.}}",
        "{{Bb:Ah ti riconosco!  Avevi lavorato in biblioteca!}}",

        "\nClara: {{Bb:...ah, Eleonora! Sì, mi ricordo di te, venivi "
        "quasi tutti i giorni.}}",

        # Options
        "\n{{yb:1: Perché la sezione privata della biblioteca è chiusa?}}",
        "{{yb:2: Perché ti stai nascondendo qui?}}",
        "{{yb:3: Conosci altra gente in paese?}}",

        "\nUsa {{lb:echo}} per fare le domande a Clara."
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Non ho più paura, Clara mi piace.}}"
    )

    def next(self):
        Step2(step_number=2)


class Step2(StepNanoStory):

    eleanors_speech = (
        "Eleonora: {{Bb:Ma che c'è di così pericoloso nella "
        "sezione privata?}}"
    )

    def next(self):
        Step3(step_number=3)


class Step3(StepNanoStory):

    eleanors_speech = (
        "Eleonora: {{Bb:Vogliamo rendere accessibile qualcosa "
        "di così pericoloso?}}"
    )

    def next(self):
        Step4()


class Step4(StepNanoStory):
    last_step = True

    print_text = "{{yb: Dove potrei trovare questo spadaccino mascherato?}}",
    story = [
        "Clara: {{Bb:Ha detto che lo}} "
        "{{lb:spadaccino mascherato}} {{Bb:vive nel bosco.}}",

        "{{Bb:Presumo che intendesse il bosco intorno alla}} "
        "{{lb:via ventosa.}}{{Bb: Quello "
        "vicino alla fattoria e a quella strana casa isolata "
        "fuori del paese.}}",

        "\n{{gb:Premi INVIO per continuare.}}"
    ]

    eleanors_speech = (
        "Eleonora: {{Bb:Uno spadaccino mascherato??}}"
    )

    def check_command(self):
        return True

    def next(self):
        play_sound("bell")
        NextStep(self.xp)
