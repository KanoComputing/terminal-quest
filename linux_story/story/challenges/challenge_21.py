#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

from linux_story.step_helper_functions import (
    unblock_cd_commands, unblock_commands_with_mkdir_hint,
    unblock_commands
)
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_22 import Step1 as NextStep


class StepTemplateMkdir(TerminalMkdir):
    challenge_number = 21


class Step1(StepTemplateMkdir):
    story = [
        "{{gb:Bellino! Hai fatto un igloo! Hai imparato una cosa nuova: "
        "il comando mkdir! (che vuol dire: fai una nuova cartella).}}",
        "\nRomina: {{Bb:Sorprendente! Per favore aiutami a fare un riparo!",
        "Si potrebbe fare nel}} {{lb:fienile}}{{Bb:, così sarà più facile "
        "metterci gli animali.}}",
        "\n{{lb:Torna}} indietro per andare {{lb:fienile}}."
    ]
    start_dir = "~/fattoria/capanno-degli-attrezzi"
    end_dir = "~/fattoria/fienile"
    deleted_items = [
        "~/fattoria/capanno-degli-attrezzi/Romina"
    ]
    story_dict = {
        "Romina": {
            "path": "~/fattoria/fienile",
        }
    }

    path_hints = {
        "~/fattoria/capanno-degli-attrezzi": {
            "blocked": "\n{{rb:Usa}} {{yb:cd ../}} {{rb:per tornare indietro.}}"
        },
        "~/fattoria": {
            "not_blocked": "\n{{gb:Buon lavoro! Ora vai nel}} {{lb:fienile}}{{gb:.}}",
            "blocked": "\n{{rb:Usa}} {{yb:cd fienile/}} {{rb:per andare nel fienile.}}"
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


class Step2(StepTemplateMkdir):
    story = [
        "Romina: {{Bb:Chiunque sarebbe capace di trovare l'igloo "
        "che hai fatto.",
        "Si potrebbe fare qualcosa di nascosto?}}\n",
        "{{yb:1: Se lo chiamiamo}} {{lb:riparo-nascosto}}"
        "{{yb:, allora sarà nascosto.}}",
        "{{yb:2: Mettendo un . prima dei nomi delle cose le rende nascoste.}}",
        "{{yb:3: È impossibile fare un riparo nascosto.}}\n",
        "Usa {{lb:echo}} per rispondere a Romina su come fare un riapro nascosto."
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = [
        "echo 1",
        "echo 2",
        "echo 3"
    ]
    hints = [
        "Romina: {{Bb:Bisogna veramente che tu sia più chiaro, "
        "Non capisco nulla di quello che dici.}}",
        "{{rb:Usa}} {{yb:echo 1}}{{rb:,}} {{yb:echo 2}} {{rb:o}} "
        "{{yb:echo 3}} {{rb:per rispondere a Romina.}}"
    ]

    def __init__(self):
        self.next_class = Step4
        StepTemplateMkdir.__init__(self)

    def check_command(self):
        if self.last_user_input == "echo 1":
            self.next_class = Step3
            return True
        elif self.last_user_input == "echo 2":
            self.next_class = Step6
            return True
        elif self.last_user_input == "echo 3":
            hint = (
                "\nRomina: {{Bb:...Davvero? Ne sei sicuro?}}"
            )
            self.send_text(hint)
        else:
            self.send_hint()

    def next(self):
        self.next_class()


# First fork - try making a hidden riparo
class Step3(StepTemplateMkdir):
    print_text = [
        "{{yb:Se lo chiamiamo}} {{lb:riparo-nascosto}}"
        "{{yb:, allora sarà nascosto.}}"
    ]
    story = [
        "Romina: {{Bb:Così, se creiamo}} {{lb:riparo-nascosto}} "
        "{{Bb:questo sarà nascosto per davvero?  Ok, proviamo.}}\n",
        "Prova a {{lb:fare}} un riparo che si chiama {{lb:riparo-nascosto}}."
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = [
        "mkdir riparo-nascosto",
    ]
    hints = [
        "{{rb:Devi fare un }} {{yb:riparo-nascosto}}"
        "{{rb:.}}",
        "{{rb:Usa il comando}} {{yb:mkdir riparo-nascosto}} "
        "{{rb:per fare il riparo.}}"
    ]

    def check_command(self):
        if self.last_user_input == "mkdir .riparo-nascosto":
            hint = (
                "\nRomina: {{Bb:Hai detto che il riparo dovrebbe chiamarsi}} "
                "{{lb:riparo-nascosto}}{{Bb:, non}} {{lb:.riparo-nascosto}}"
                "{{Bb:.}}"
                "\n{{yb:Premi la freccia in SÙ, e cambia il comando.}}"
            )
            self.send_text(hint)
        else:
            return StepTemplateMkdir.check_command(self)

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "{{lb:Guarda in giro}} per vedere se è davvero nascosto."
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = [
        "ls"
    ]
    hints = [
        "{{rb:Guarda intorno}} {{yb:ls}}{{rb:.}}"
    ]
    ls_a_hint = True

    def check_command(self):
        if self.last_user_input == "ls -a" and self.ls_a_hint:
            hint = (
                "\n{{gb:Quasi!}} {{ob:Ma devi controllare "
                "se il riparo è nascosto, quindi non guardare "
                "attorno}} {{yb:troppo attentamente}}{{rb:.}}"
            )
            self.send_text(hint)
            self.ls_a_hint = False
        else:
            return StepTemplateMkdir.check_command(self)

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Romina: {{Bb:Hai fatto un}} {{lb:riparo-nascosto}}{{Bb:!}}",
        "{{Bb:...Il problema è che lo vedo anch'io.  Non mi sembra che funzioni.",
        "Come si potrebbe fare per renderlo nascosto?}}",
        "\n{{yb:1: Se metti un . davanti al nome, allora diventa nascosto.}}",
        "{{yb:2: Ti sbagli. Non puoi vedere il riparo-nascosto, è "
        "nascosto.}}\n",
        "Usa {{lb:echo}} per parlare a Romina.",
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = [
        "echo 1"
    ]
    hints = [
        "Romina: {{Bb:DEVI parlare in modo più chiaro. Non ti capisco.}}",
        "{{rb:Usa}} {{yb:echo 1}} {{rb:o}} {{yb:echo 2}} {{rb:per rispondere.}}"
    ]

    def check_command(self):
        if self.last_user_input == "echo 1":
            return True

        elif self.last_user_input == "echo 2":
            hint = (
                "\nRomina: {{Bb:....",
                "Attento ragazzo, mica sono scema. Codesto riparo non è nascosto.\n"
                "Come faccio a farne uno che lo sia davvero?}}"
            )
            self.send_text(hint)

        else:
            self.send_hint()

    def next(self):
        Step6()


###########################################
# Second fork

class Step6(StepTemplateMkdir):
    print_text = [
        "{{yb:Se metti un . davanti al nome diventa nascosto.}}"
    ]
    story = [
        "Romina: {{Bb:Così se chiamiamo il riparo}} {{lb:.riparo}}"
        "{{Bb:, questo diventa nascosto?  Proviamo!}}",
        "{{lb:Costruiamo}} un riparo che si chiama {{lb:.riparo}}"
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"

    hints = [
        "{{rb:Fai un}} {{lb:.riparo}} {{rb:usando}} {{yb:mkdir .riparo}}"
        "{{rb: - ricorda il punto!}}"
    ]
    commands = [
        "mkdir .riparo"
    ]

    def block_command(self):
        return unblock_commands_with_mkdir_hint(
            self.last_user_input, self.commands
        )

    def next(self):
        Step7()


class Step7(StepTemplateMkdir):
    story = [
        "Controlla che sia nascosto per bene. Usa {{yb:ls}} per "
        "vedere se è visibile."
    ]

    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"

    commands = [
        "ls"
    ]

    hints = [
        "{{rb:Usa}} {{yb:ls}}{{rb:, non ls -a, per controllare se il tuo riparo "
        "è nascosto.}}"
    ]

    def next(self):
        Step8()


class Step8(StepTemplateMkdir):
    story = [
            "{{gb:Bene, ora nel fienile non si vede.}}",
        "Ora guardiamo con {{yb:ls -a}} per essere sicuri che invece esista!"
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    commands = [
        "ls -a"
    ]
    hints = [
        "{{rb:Usa}} {{yb:ls -a}} {{rb:per guardare attorno.}}"
    ]

    def next(self):
        Step9()


class Step9(StepTemplateMkdir):
    story = [
        "{{gb:Ha funzionato! Ti è riuscito di creare un oggetto nascosto.}}",
        "\nRomina: {{Bb:Hai creato per davvero qualcosa? Non ci posso credere!",
        "...sfortunatamente non lo posso vedere...puoi condurrmi dentro "
        "insieme agli animali?}}\n",
        "{{lb:Sposta}} tutti nel {{lb:.riparo}}, "
        "uno per uno.\n"
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile"
    all_commands = [
        "mv Trogolo .riparo/",
        "mv Trogolo .riparo",
        "mv Violetta .riparo/",
        "mv Violetta .riparo",
        "mv Gelsomino .riparo/",
        "mv Gelsomino .riparo",
        "mv Romina .riparo/",
        "mv Romina .riparo"
    ]

    def block_command(self):
        return unblock_commands(self.last_user_input, self.all_commands)

    def check_command(self):

        # If we've emptied the list of available commands, then pass the level
        if not self.all_commands:
            return True

        # If they enter ls, say Well Done
        if self.last_user_input == 'ls' or self.last_user_input == "ls -a":
            hint = "\n{{gb:Well done for looking around.}}"
            self.send_text(hint)
            return False

        # check through list of commands
        end_dir_validated = False
        self.hints = [
            "{{rb:Usa}} {{yb:" + self.all_commands[0] + "}} "
            "{{rb:per andare avanti}}"
        ]

        end_dir_validated = self.current_path == self.end_dir

        # if the validation is included
        if self.last_user_input in self.all_commands and \
                end_dir_validated:

            # Remove both elements, with a slash and without a slash
            if self.last_user_input[-1] == "/":
                self.all_commands.remove(self.last_user_input)
                self.all_commands.remove(self.last_user_input[:-1])
            else:
                self.all_commands.remove(self.last_user_input)
                self.all_commands.remove(self.last_user_input + "/")

            if len(self.all_commands) == 2:
                hint = (
                    "\n{{gb:Bella prova! Spostane un altro nel}}"
                    " {{yb:.riparo}}"
                )
            elif len(self.all_commands) > 2:
                hint = "\n{{gb:Ottimo! spostane altri " + \
                    str(len(self.all_commands) / 2) + \
                    ".}}"
            else:
                hint = "\n{{gb:Premi Invio per continuare}}"

            self.send_text(hint)

        else:
            self.send_text("\n" + self.hints[0])

        # Always return False unless the list of valid commands have been
        # emptied
        return False

    def next(self):
        Step10()


class Step10(StepTemplateMkdir):
    story = [
        "{{lb:Vai}} nel {{lb:.riparo}} insieme a Romina e "
        "gli animali."
    ]
    start_dir = "~/fattoria/fienile"
    end_dir = "~/fattoria/fienile/.riparo"
    hints = [
        "{{rb:stampa}} {{yb:cd .riparo/}} {{rb:per andare nel}} "
        "{{lb:.riparo}}{{rb:.}}"
    ]

    def block_command(self):
        return unblock_cd_commands(self.last_user_input)

    def next(self):
        Step11()


class Step11(StepTemplateMkdir):
    story = [
            "Dai {{lb:un'occhiata intorno}} per controllare di avere spostato tutti."
    ]
    start_dir = "~/fattoria/fienile/.riparo"
    end_dir = "~/fattoria/fienile/.riparo"
    commands = [
        "ls",
        "ls -a"
    ]
    hints = [
        "{{rb:Guarda attorno con}} {{yb:ls}}{{rb:.}}"
    ]
    last_step = True

    def next(self):
        NextStep(self.xp)
