#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story


from ..Step import Step
from ..terminals.terminal2 import Terminal2


class Step_Template(Step):

    def launch_terminal(self):
        Terminal2(self.start_dir, self.end_dir, self.command, self.hint)


class Step1(Step_Template):
    story = [
        "You are in the home directory.",
        "You remember the rabbit's note, "
        "which told you to look harder around here"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls -a"
    hint = [
        "You decide that the rabbit meant that you should look "
        "for hidden files and folders in this directory",
        "To see any hidden folders or files you need to "
        "{{yl}}i{{ys}}t {{ya}}ll the files and folders",
        "The command {{yls -a}} lists all files and folders in a directory",
        "Type {{yls -a}} and press ENTER"
    ]

    def next(self):
        Step2()


class Step2(Step_Template):
    story = [
        "You see a small shady {{b.hidden-path}} you didn't notice before.",
        "Can you see what's down the path?"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ["ls .hidden-path", "ls .hidden-path/"]
    hint = [
        "The command {{yls <Directory name>}} lets you look into a directory",
        "To look down the hidden path, type {{yls .hidden-path}}",
        "Type {{yls .hidden-path}} and press ENTER"
    ]

    def next(self):
        Step3()


class Step3(Step_Template):
    story = [
        "Squinting, you can just about see the path "
        "leading to a dense thicket of woodland",
        "You decide to walk down the path",
        "You need to use the command {{ycd}} to {{yc}}hange {{yd}}irectory",
        "First, use {{y cd .hidden-path}} to go on the {{b.hidden-path}}"
    ]
    start_dir = "~"
    end_dir = ".hidden-path"
    command = ""
    hint = [
        "You want to {{yc}}hange your {{yd}}irectory so are in the .hidden-path "
        "directory",
        "You want to use the command {{ycd <path to directory>}} "
        "to get into the directory",
        "Use the command {{ycd .hidden-path}}"
    ]

    def next(self):
        Step4()


class Step4(Step_Template):
    story = [
        "Have another look around"
    ]
    start_dir = ".hidden-path"
    end_dir = ".hidden-path"
    command = "ls"
    hint = [
        "To look around, you need to {{yl}}i{{ys}}t all the files in the directory",
        "Use {{yls}} to look around you.",
        "Type {{yls}} and press Enter"
    ]

    def next(self):
        Step5()


class Step5(Step_Template):
    story = [
        "You are on the narrow dusty path leading into the woods",
        "You decide to walk into the woods"
    ]
    start_dir = ".hidden-path"
    end_dir = "woods"
    command = ""
    hint = [
        "Remember, you want to {{yc}}hange your {{yd}}irectory to the {{bwoods}} "
        "directory",
        "Type {{ycd woods}} and press Enter"
    ]

    def next(self):
        Step6()


class Step6(Step_Template):
    story = [
        "Have a look around."
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = ["ls", "ls -a"]
    hint = [
        "To look around, you need to use the command {{yls}}"
    ]

    def next(self):
        Step7()


class Step7(Step_Template):
    story = [
        "You see you're surrounded by a lot of plants, trees and shubbery.",
        "There's a lot of stuff here, but you have sharp eyes and take a good look round "
        "you",
        "You're looking for a hidey-hole for a rabbit",
        "When you find it, you want to enter it"
    ]
    start_dir = "woods"
    end_dir = "rabbithole"
    command = ""
    hint = [
        "Remember, {{bdirectories show up in blue}}",
        "If you scroll through the elements in this directory, you should be able to "
        "spot the rabbit's because it will be the only {{bblue}} one",
        "Remember, you want to {{yc}}hange the {{yd}}irectory to the directory you find."
    ]

    def next(self):
        Step8()


class Step8(Step_Template):
    story = [
        "You entered the rabbithole",
        "The rabbit who dug it must be huge, the rabbithole is bigger than the average "
        "man",
        "Let's clear the terminal to end this challenge"
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "clear"
    hint = [
        "Type {{yclear}} and press Enter to clear the terminal"
    ]


"""
class Step7(Step):
    story = [
        "You see you're surrounded by a lot of plants, trees and shubbery.",
        "There's a lot of stuff here, but you don't think you can spot anything useful.",
        "It occurs to you that the rabbit would probably hide his hidey-hole"
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "ls -a"
    hint = [
        "You want to use the command we used to show hidden files and directories",
        "The command you're looking for "
        "{{yl}}i{{ys}}ts {{ya}}ll the files and directories",
        "Use the command {{yls -a}} to show all hidden files and directories",
        "Type {{yls -a}} and press Enter"
    ]

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step8()


class Step6(Step):
    story = [
        "There's too much really for you to see clearly",
        "What would be good is if you could filter through the files",
        "Ideally you only want to see the hidden files, "
        "or the files/directories starting with .",
        "{{yls -d}} allows you to filter information about the directory you are in.",
        "For example {{yls -d}} will show you the directory you're in",
        "Try it!"
    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "ls -d"
    hint = [
        "Run the command {{yls -d}}"
    ]

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step7()


class Step7(Step):
    story = [
        "The command shows the current directory, which is always represented by .",
        "We can look in the directory for filtered information "
        "by adding information we do know",
        "We only want to see files and directories starting with .",
        "The character * represents any character. "
        "So {{yls -d .*}} should show everything starting with ."

    ]
    start_dir = "woods"
    end_dir = "woods"
    command = "ls -d .*"
    hint = [
        "Run the command {{yls -d .*}}"
    ]

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step8()


class Step9(Step):
    story = [
        "You see a rabbithole hidden behind one of the trees",
        "The rabbit that dug it must be huge.  "
        "It looks big enough for you to squeeze through."
    ]
    start_dir = "woods"
    end_dir = "cd .rabbithole"
    command = ""
    hint = [
        "Enter the rabbithole",
        "Type the command {{ycd .rabbithole}}"
    ]

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step9()
"""
