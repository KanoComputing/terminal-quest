#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story


from ..Step import Step
#from challenge_2a import Step1 as Step1_2


class Step1(Step):
    story = [
        "Hello there",
        "{{rW}}{{oe}}{{yl}}{{gc}}{{bo}}{{pm}}{{re}} to"
        " the dark side of the Kano OS.",
        "Type {{yls}} (short for {{yl}}i{{ys}}t) to have a look around.",
        "You are in a dark room."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls"
    hint = ["Type {{yls}} and press Enter to have a look around."]

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step2()


class Step2(Step):
    story = [
        "\nThe room is no longer dark."
        "You see the door to an Office.",
        "{{yls <Directory Name>}} lets you look into the directory",
        "The office door has a window.  Have a look into the office."
    ]
    start_dir = "~"
    end_dir = "~"
    command = "ls Office"
    hint = "Type the command {{yls Office}}"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step3()


class Step3(Step):
    story = [
        "\nTry walking into the Office.",
        "The command {{ycd <Directory Name>}} allows you to {{yc}}hange {{d}}irectory",
        "The door looks unlocked."
    ]
    start_dir = "~"
    end_dir = "Office"
    command = ""
    hint = "Type the command {{ycd Office}}"

    def __init__(self):
        Step.__init__(self)

    def next(self):
        Step4()


class Step4(Step):
    story = [
        "\nYou are now inside the Office.",
        "It is dark."
    ]
    start_dir = "Office"
    end_dir = "Office"
    command = "ls"
    hint = ["Remember the command for looking around you?  You used it at the start",
            "The command {{yls}} shows what files and directories are around you",
            "Type {{yls}} and press Enter"]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step5()


class Step5(Step):
    story = [
        "\nYou can see the files and directories available in this directory",
        "Files are shown in green, directories in blue",
        "Explore this office.  See what information is in here",

    ]
    start_dir = "Office"
    end_dir = "Office"
    command = "ls Missions"
    hint = [
        "",
        "",
        "Remember that {{yls <directory name>}} "
        "{{yl}}i{{ys}}ts the files inside a directory",
        "Type {{yls Missions}}"
    ]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step6()


class Step6(Step):
    story = [
        "\nYou see an paper report titled \"Rabbit Report\".",
        "It has TOP SECRET stamped in the corner",
        "To read a file, you use the command {{yless}}"
    ]
    start_dir = "Office"
    end_dir = "Office"
    command = "ls Missions"
    hint = [
        "To read a file, type {{yless filename}}",
        "Type {{yless Rabbit_Report}} to read the rabbit report"
    ]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step7()


class Step7(Step):
    story = [
        "You get the feeling there is something hidden in this room",
        "To view hidden files and directories, "
        "use the command {{yls -a}} (to {{yl}}i{{ys}}t {{ya}}"
    ]
    start_dir = "Office"
    end_dir = "Office"
    command = "ls -a"
    hint = [
        ""
    ]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step8()


class Step8(Step):
    story = [
        "You notice the sticky note on the desk.",
        "The command {{ycat}} or {{yless}} will allow you "
        "to read what's written on the note"
    ]
    start_dir = "Office"
    end_dir = "Office"
    command = ["cat .sticky_note", "less .sticky_note"]
    hint = [
        "Type {{ycat .sticky_note}} to see what's written on the note."
    ]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step9()


class Step9(Step):
    story = [
        "You decide you've found everything there is in this Office for the time being.",
        "The directory previous is referred to as ..",
        "So to go back a directory, the command is {{ycd ..}}"
    ]
    start_dir = "Office"
    end_dir = "~"
    command = ""
    hint = [
        "Type {{ycd ..}} to see what's written on the note."
    ]

    def __init__(self):

        Step.__init__(self)

    def next(self):
        Step10()


class Step10(Step):
    story = [
        "Lastly, you decide you want to clean up your screen.",
        "The command {{yclear}} clears the writing on the terminal"
    ]
    start_dir = "~"
    end_dir = "~"
    command = "clear"
    hint = [
        "Type {{yclear}} to clear the Terminal."
    ]

    def __init__(self):
        Step.__init__(self)
