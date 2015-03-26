
import os
from linux_story.Step import Step


'''
chapter 3

What other hidden files could be around here?  Have a look around with ls -a
Go around the rooms with ls -a
(Can level up when all the hidden files we've hidden have been shown)

.safe-box (parent's room, containing journal, money and ECHO)
journal entry:
$USERNAME is so quiet, I'm a bit worried.  Andrea is a talkative woman, maybe we should go and

.diary (your room) (empty? "Looks like you don't write in it very often")
.footprints

With ECHO, suggest they move it to your chest.
Then go to town to talk to the
'''


class StepTemplate(Step):
    def __init__(self):


class Step1(StepTemplate):
    story = [
        "You are in your room, standing in front of the .chest containing all",
        "the comands you've learnt so far",
        "Could there be anything else around here?",
        "Maybe something else is hidden in the house?",
        "Have you looked in your parent's room yet?"
    ]
    start_dir = "my-room"

    # Keep this unspecified
    end_dir = ""

    # Want to check your parents room
    hints = ["Is there anything in your parent's room?"]

    challenge_number = 17

    def check_output(self, output):
        # Want output to contain the .journal file from your mum

        if '.journal' in output:
            return True

        else:
            return False


class Step2(StepTemplate):
    story = [
        "So you found your mum's journal?",
        "You probably shouldn't read it...",
        "What else is here?"
    ]

    def __init__(self):
        self.check_diary = 0

    def check_command(self, command):
        # Check to see if the kid reads his/her Mum's journal
        if command == 'cat .journal' and check_diary == 0:
            self.send_hint('You read your Mum\'s diary!  -5XP for you!')
            self.check_diary += 1
            return False

    def check_output(self, output):
        # Check to see if the kid read his/her Mum's journal
        if 'Dear Diary' in output and check_diary == 0:
            self.send_hint('You read your Mum\'s diary!  -5XP for you!')
            self.check_diary += 1
            return False

        # Compare output string with a string you know will be in the map
        elif '  Farm  ' in output:
            return True


class Step3(StepTemplate):
    story = [
        "So there's a map leading to a farm?",
        "Apparently it's not far from our house, just off the windy road",
        "Have we noticed this before?",
        "Let's look out for it this time!",
        "What is this ECHO note?  Maybe we should move it into the chest?"
    ]

    hint = [
        "Move the {{yb:mv}} command into your {{yb:chest}} in your {{yb:room}}"
    ]

    def check_output(self, output):
        # This is run after the command has been run, so can check for the
        # existance of a file now

        ECHO_path = ''
        if os.file.exists(ECHO_path):
            return True

        return False


class Step4(StepTemplate):
    story = [
        "Now let's head to ~ to find the farm!",
        "Type {{yb:cd}} by itself to go to ~"
    ]

    hint = [
        "Use {{yb:cd}} by itself to go to ~"
    ]

    start_dir = "parents-room"
    end_dir = "~"


class Step5(StepTemplate):
    story = [
        "You are back on the windy road, which stretches endlessly in both directions.
        Look around."
    ]

    command = "ls"
    start_dir = '~'
    end_dir = '~'


class Step6(StepTemplate):
    story = [
        "You notice a small remote farm in the distance.",
        "Go towards it."
    ],

    start_dir = "~"
    end_dir = "farm"


class Step7(StepTemplate):
    story = [
        "Look around."
    ]

    command = "ls"
    start_dir = "farm"
    end_dir = "farm"


class Step8(StepTemplate):
    story = [
        "You are in a well tended plot of land, with chickens and animals",
        "There must be people present here.  See if you can find someone to talk to."
    ]

    def check_output(self):


