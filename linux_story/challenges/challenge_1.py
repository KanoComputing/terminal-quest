#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story


from ..Step import Step
from kano.network import is_internet


class Step1(Step):
    story = [
        "Hello there",
        "{{rW}}{{oe}}{{yl}}{{gc}}{{bo}}{{pm}}{{re}} to"
        " the dark side of the Kano OS.",
        "Have a look around",
        "Type {{yls}} (short for {{yl}}i{{ys}}t) to see where you are."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls"
    hint = "Type the command \"ls\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "\nWoah, do you see that",
        "There's a rabbithole!",
        "Type {{ycd rabbithole}} (stands for {{yc}}hange {{yd}}irectory"
        " to {{yrabbithole}})"
    ]
    start_dir = "~"
    end_dir = "rabbithole"
    command = ""
    hint = "Type the command \"cd rabbithole\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = ["\nAwesome.  Take another look around."]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "ls"
    hint = "Type the command \"ls\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step4()


class Step4(Step):
    story = [
        "\nThere's a sign on the wall",
        "Let's read what it says",
        "The command {{ycat}} shows the text contained in a file",
        "Use the command {{ycat scribbled_note}}"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "cat scribbled_note"
    hint = "Type the command \"cat scribbled_note\""

    def __init__(self):

        Step.__init__(self)

    def next(self):
        if is_internet():
            from challenge_2a import Step1 as Step1_2
        else:
            from challenge_2b import Step1 as Step1_2
        Step1_2()
