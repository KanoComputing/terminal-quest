#!/usr/bin/env python
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Author: Caroline Clark <caroline@kano.me>
# A chapter of the story

import os
import sys

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)
        print sys.path

from linux_story.Step import Step
from terminals import Terminal1, Terminal2, Terminal3
#from linux_story.file_data import copy_data
#from linux_story.helper_functions import print_challenge_title
#from linux_story.file_functions import write_to_file


class Step_Template1(Step):
    def __init__(self):
        Step.__init__(self, Terminal1)


class Step_Template2(Step):
    def __init__(self):
        Step.__init__(self, Terminal2)


class Step_Template3(Step):
    def __init__(self):
        Step.__init__(self, Terminal3)


class Step1(Step_Template1):
    story = [
        "....",
        ".......",
        "Wh..What time is it?",
        "Wow it's dark in here. I can't see a thing!",
        "Type {{yls}} to take a look around."
    ]
    start_dir = "room"
    end_dir = "room"
    command = "ls"
    hints = ["Type {{yls}} and press Enter to have a look around."]

    def next(self):
        Step2()


class Step2(Step_Template2):
    story = [
        "\nI'm in my bedroom! I must have fallen asleep watching that movie.",
        "Wow, I forgot how much cool stuff I have in my room. Let's take a look!",
        "You can use {{ycat}} and the name of an object to learn more about it!",
        "Try {{ycat tv}} to get started"
    ]
    start_dir = "room"
    end_dir = "room"
    command = "cat tv"
    hints = "Type the command {{ycat tv}}"

    def next(self):
        Step3()


class Step3(Step_Template2):
    story = [
        "\nI can't even remember what the movie was about!",
        "Let's use {{yls}} again to print a {{ylist}} of the things in my room."
    ]
    start_dir = "room"
    end_dir = "room"
    command = "ls"
    hints = [
        "Type the command {{yls}}"
    ]

    def next(self):
        Step4()


class Step4(Step_Template2):
    story = [
        "\nThere's some more things on my shelf. Let's take a look!",
        "Type {{yls shelves}} to see what's on the shelf"
    ]
    start_dir = "room"
    end_dir = "room"
    command = ["ls shelves", "ls shelves/"]
    hints = [
        "Remember that {{yls <directory name>}} "
        "{{yl}}i{{ys}}ts the files inside a directory",
        "Type {{yls shelves}} and press Enter"
    ]

    def next(self):
        Step5()


class Step5(Step_Template2):
    story = [
        "\nOh wow - I forgot about some of these. Let's have a look at them.",
        "Type {{ycat shelves/comic-book}} to look inside the comic book"
    ]
    start_dir = "room"
    end_dir = "room"
    command = [
        "cat shelves/comic-book"
    ]
    hints = [
        "Type {{ycat shelves/comic-book}} to look inside!"
    ]

    def next(self):
        Step6()


class Step6(Step_Template2):
    story = [
        "\nYou can look at the other books too! Use {{ycat shelves/<bookname>}} to take a peek."
    ]
    start_dir = "room"
    end_dir = "room"
    command = "cat shelves/war-and-peace"
    hints = [
        "Read another book by using {{ycat}}",
        "Type {{ycat war-and-peace}} to look at your war-and-peace book"
    ]

    def next(self):
        Step7()


class Step7(Step_Template2):
    story = [
        "I better get dressed. Let's see what's in the wardrobe.",
        "Type {{yls wardrobe}} to see what we have to wear!"
    ]
    start_dir = "room"
    end_dir = "room"
    command = ["ls wardrobe", "ls wardrobe/"]
    hints = [
        "Type {{yls wardrobe}} to see what we have to wear!"
    ]

    def next(self):
        Step8()


class Step8(Step_Template2):
    story = [
        "Let's choose something to wear.",
        "Type {{ycat warbrobe/hat}}"
    ]
    start_dir = "room"
    end_dir = "room"
    command = ["cat wardrobe/hat"]
    hints = [
        "Type {{ycat warbrobe/hat}} to look at the hat."
    ]

    def next(self):
        Step9()


class Step9(Step_Template3):
    story = [
        "I really like this one! I think I'll wear it.",
        "I hear mum calling from the kitchen.",
        "\"Halloooo?? Are you awake? Come and get your breakfast!\"",
        "Let's go to the kitchen!",
        "Type {{ycd}} to go to the home folder"
    ]
    start_dir = "room"
    end_dir = "~"
    command = ""
    hints = [
        "Type {{ycd}} to go to the home folder."
    ]

    def next(self):
        Step10()


class Step10(Step_Template3):
    story = [
        "Now we need to go to the kitchen.",
        "Have a look around you around using {{yls}}"
    ]
    start_dir = "~"
    end_dir = "~"
    command = ""
    hints = [
        "Type {{yls}} to look around."
    ]

    def next(self):
        Step11()


class Step11(Step_Template3):
    story = [
        "I see the door to the kitchen!",
        "To go to the kitchen, type {{ycd kitchen}}"
    ]
    start_dir = "~"
    end_dir = "kitchen"
    command = ""
    hints = [
        "Type {{ycd kitchen}} to go to the kitchen."
    ]

    def next(self):
        Step12()


class Step12(Step_Template3):
    story = [
        "Where is Mum? Use {{yls}} to {{ylist}} what's in the kitchen."
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "ls"
    hints = [
        "Use {{yls}} to {{ylist}} what's in the kitchen."
    ]

    def next(self):
        Step13()


class Step13(Step_Template3):
    story = [
        "There she is! Go talk to her.",
        "Remember {{ycat}}? Use it again!"
    ]
    start_dir = "kitchen"
    end_dir = "kitchen"
    command = "cat kitchen"
    hints = [
        "Type {{ycat kitchen}}."
    ]

    def next(self):
        Step14()


class Step14(Step_Template3):
    story = [
        "Now we want to go to the garden ",
        "Use {{ycd}} to move home."
    ]
    start_dir = "kitchen"
    end_dir = "~"
    command = ""
    hints = [
        "Use {{ycd}} to move back to your home."
    ]

    def next(self):
        Step15()


class Step15(Step_Template3):
    story = [
        "Now we want to go to the garden",
        "Use {{ycd}} to move your current position."
    ]
    start_dir = "~"
    end_dir = "garden"
    command = ""
    hints = [
        "Use {{ycd garden}} to move back to your room."
    ]

    def next(self):
        Step16()


class Step16(Step_Template3):
    story = [
        "You're in the garden - let's take a look around!"
    ]
    start_dir = "garden"
    end_dir = "garden"
    command = "ls"
    hints = [
        "What was the command for {{yList}} again? If you get stuck - check out the spell book below",
        "Type {{yls}} to show everything in the garden"
    ]

    def next(self):
        Step17()


class Step17(Step_Template3):
    story = [
        "When you're ready, enter {{ycd greenhouse}} to go and see Dad."
    ]
    start_dir = "garden"
    end_dir = "greenhouse"
    command = ""
    hints = [
        "Enter {{ycd greenhouse}} to go and see Dad."
    ]

    def next(self):
        Step18()


class Step18(Step_Template3):
    story = [
        "Use {{yls}} to look around."
    ]
    start_dir = "greenhouse"
    end_dir = "greenhouse"
    command = "ls"
    hints = [
        "Enter {{yls}} to have a look around."
    ]
