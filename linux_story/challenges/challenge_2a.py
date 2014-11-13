#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story


from ..Step import Step
from challenge_3 import Step1 as Step1_next


class Step1(Step):
    story = [
        "The rabbit left us a message",
        "We should reply back to him",
        "Type {{ynano scribbled_note}} to edit the rabbit's note"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "nano scribbled_note"
    hint = "Type the command \"nano scribbled_note\" and" \
        " write your own message to the rabbit"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "Awesome, now let's have a look around some more.",
        "How about looking for all the hidden files?",
        "Type {{yls -a}} (which stands for {{yl}}i{{ys}}t {{ya}}ll)"
        " to look at all the files in a directory"
    ]
    start_dir = "rabbithole"
    end_dir = "rabbithole"
    command = "ls -a"
    hint = "Type the command 'ls -a'"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "Look!  {{yls -a}} lets us see all the files and directories with a ."
        " at the start",
        "These files are normally hidden from view",
        "There's a .trapdoor directory, and a .key file.",
        "Do we need the .key file?  The .trapdoor looks open...",
        "Type {{ycd .trapdoor}} to go into the trapdoor"
    ]
    start_dir = "rabbithole"
    end_dir = ".trapdoor"
    command = ""
    hint = "Type the command 'cd .trapdoor'"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step4()


class Step4(Step):
    story = [
        "It looks like we got in",
        "What's in this directory?",
        "Have a look around"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "ls"
    hint = "Type the command 'ls'"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step5()


class Step5(Step):
    story = [
        "Look, there's another note",
        "What does this one say?"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    commands = [
        "less second_scribbled_note",
        "cat second_scribbled_note",
        "more second_scribbled_note"
    ]
    hint = "Type the command \"cat second_scribbled_note\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step6()


class Step6(Step):
    story = [
        "Why did the rabbit say we couldn't make changes to it?",
        "Ha, lets show it!  Try editing the note using 'nano'"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    commands = "nano second_scribbled_note"
    hint = "Type the command \"nano second_scribbled_note\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step7()


class Step7(Step):
    story = [
        "Wait, we can't make any changes to the note the rabbit left",
        "To check the permissions of a file, use the command "
        "{{yls -l}} (which stands for {{yl}}ong listing)"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "ls -l"
    hint = "Type the command \"ls -l\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step8()


class Step8(Step):
    story = [
        "That's a lot of info!",
        "Let's break up what it means",
        "We get blocks of info of the form",
        "-r--r--r- means that the file is readable, but not writable.",
        "If the file was writable, it would have permissions -rw-rw-r-",
        "Since we can't edit the rabbit's note, let's create our own.",
        "Use the command 'touch note', which creates a new file called 'note'"
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "touch note"
    hint = "Type the command \"touch note\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step9()


class Step9(Step):
    story = ["If you use 'ls', you'll see the new file you've created"],
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "ls"
    hint = "Type the command \"ls\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step10()


class Step10(Step):
    story = [
        "Now let's edit the note using 'nano'.  Write a message and save it."
    ]
    start_dir = ".trapdoor"
    end_dir = ".trapdoor"
    command = "nano note"
    hint = "Type the command \"nano note\""

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step1_next()
