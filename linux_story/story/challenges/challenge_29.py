#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A chapter of the story

import os
from linux_story.story.terminals.terminal_eleanor import TerminalNanoEleanor
from linux_story.story.challenges.challenge_30 import Step1 as NextStep
from linux_story.helper_functions import play_sound


# Can't get all the information with this system unless you are interested.
story_replies = {
    "echo 1": [
        {
            "user": "Why are you hiding down here?",
            "clara": (
                "Clara: {{Bb:I heard a bell ring, and saw the "
                "lead librarian disappear in front of me. I was "
                "so scared I ran away, and found this .cellar here.}}"
            )
        },
        {
            "user": "What do you think that bell is?",
            "clara": (
                "Clara: {{Bb:There's a legend that says there's a bell that "
                "calls a pet to its master. So maybe the bell is "
                "nothing to be afraid of?  At least, I hope so..."
            )
        },
        {
            "user": "Do you have any relatives in town?",
            "clara": (
                "I had a couple of children, a {{lb:young-boy}} and a "
                "{{lb:little-girl}}. I hope they are alright."
            )
        },
        {
            "user": "echo 1 Question 4",
            "clara": (
                "echo 1 Answer 4"
            )
        }
    ],

    "echo 2": [
        {
            "user": "Why is the private section locked?",
            "clara": (
                "Clara: {{Bb:It contains some powerful information."

                "\n...I'm sorry, I shouldn't say more. The head librarian "
                "was quite concerned that no one should go in.}}"
            )
        },
        {
            "user": "How did you lock the protected section?",
            "clara": (
                "Clara: {{Bb:I didn't! The only person that could do that "
                "was lead librarian."

                "\nHe had to find a special command to be able to do that.}}"
            )
        },
        {
            "user": "What was the command he used to lock it?",
            "clara": (
                "Clara: {{Bb:He didn't teach me it, I wasn't senior enough "
                "to learn it.}}"

                "\n{{Bb:I think he found it from this strange}} "
                "{{lb:masked swordsmaster}} {{Bb:outside of town.}}"

                "\nHe recorded the command, but it was stolen from the "
                "library."
            )
        },
        {
            "user": "Where would I find this masked swordsmaster?",
            "clara": (
                "Clara: {{Bb:He said the}} "
                "{{lb:masked swordsmaster}} {{Bb:lived in the woods.}}"

                "\n{{Bb:I presume he meant the woods just off the}} "
                "{{lb:Windy Road}}{{Bb:? The one "
                "near the farm and that funny lonely house outside town.}}"
            )
        }
    ],

    "echo 3": [
        {
            "user": "Do you know any other people in town?",
            "clara": (
                "Clara: {{Bb:There's a man I don't trust that runs the "
                "shed-shop. I think his name is Bernard.}}"
            )
        },
        {
            "user": "Why don't you like Bernard?",
            "clara": (
                "Clara: {{Bb:He makes very simple tools and charges a fortune "
                "for them.}}"
                "\n{{Bb:His father was a very clever man and would spend all "
                "his time in the library reading up commands. He became a "
                "successful business man as a result."
            )
        },
        {
            "user": "Why is the library so empty?",
            "clara": (
                "Clara: {{Bb:We should have introduced late fees a long "
                "time ago...}}"
            )
        },
        {
            "user": "echo 3 Question 4",
            "clara": (
                "echo 3 Answer 4"
            )
        }
    ]
}


# Generate the story from the step number
def create_story(step):
    print_text = ""

    if step > 1:
        print_text = "{{yb:" + story_replies["echo 2"][step - 2]["user"] + "}}"

    story = [
        story_replies["echo 2"][step - 2]["clara"],
        "\n{{yb:1: " + story_replies["echo 1"][0]["user"] + "}}",
        "{{yb:2: " + story_replies["echo 2"][step - 1]["user"] + "}}",
        "{{yb:3: " + story_replies["echo 3"][0]["user"] + "}}"
    ]

    # print "print_text = {}".format(print_text)
    # print "story = {}".format(story)

    return (print_text, story)


# Want to eliminate the story that the user has already seen
def pop_story(user_input):
    # if the user_input is echo 1, echo 2 or echo 3
    if user_input in story_replies:
        reply = story_replies[user_input][0]
        # print "reply = {}".format(reply)
        # print "story_replies = {}".format(story_replies)
        story_replies[user_input].remove(reply)
        return reply


class StepTemplateNano(TerminalNanoEleanor):
    challenge_number = 29

    commands = [
        "echo 2"
    ]

    start_dir = "~/town/east-part/restaurant/.cellar"
    end_dir = "~/town/east-part/restaurant/.cellar"
    echo_hit = {
        "echo 1": True,
        "echo 3": True
    }

    def check_command(self, current_dir):

        # If self.last_user_input equal to "echo 1" or "echo 3"
        if self.last_user_input in story_replies:

            if self.last_user_input == "echo 2":
                return True
            else:
                if self.echo_hit[self.last_user_input]:
                    self.echo_hit[self.last_user_input] = False
                    reply = pop_story(self.last_user_input)["clara"]
                    self.send_text("\n" + reply)

        else:
            return TerminalNanoEleanor.check_command(self, current_dir)


class Step1(StepTemplateNano):
    story = [
        "Clara: {{Bb:What? Who are you?}}",

        "\nEleanor: {{Bb:Hello! I'm Eleanor, and this is}} {{gb:" +
        os.environ["LOGNAME"] + "}}{{Bb:.}}",
        "{{Bb:I recognise you!  You used to work in the library!}}",

        "\nClara: {{Bb:...ah, Eleanor! Yes, I remember you, you used to "
        "come in almost everyday.}}",

        # Options
        "\n{{yb:1: Why are you hiding down here?}}",
        "{{yb:2: Why is the protected-section locked?}}",
        "{{yb:3: Do you know about any other people in town?}}",

        "\nUse {{lb:echo}} to ask Clara a question."
    ]

    eleanors_speech = (
        "Eleanor: {{Bb:I'm not scared anymore, I like Clara.}}"
    )

    def next(self):
        Step2()


class Step2(StepTemplateNano):
    print_text = [create_story(2)[0]]
    story = create_story(2)[1]

    # print "Step2 print_text = {}".format(print_text)
    # print "Step2 story = {}".format(story)

    def next(self):
        Step3()


class Step3(StepTemplateNano):
    print_text = [create_story(3)[0]]
    story = create_story(3)[1]
    # (print_text, story) = create_story(3)

    def next(self):
        Step4()


class Step4(StepTemplateNano):
    print_text = [create_story(4)[0]]
    story = create_story(4)[1]
    last_step = True

    def next(self):
        play_sound("bell")
        NextStep(self.xp)


'''
class Step3(StepTemplateNano):
    print_text = [
        "{{yb:How did you lock the protected-section}}"
    ]

    story = [
        "Clara: {{Bb:I didn't! The only person that could do that "
        "was lead librarian."

        "\nHe had to find a special command to be able to do that. "
        "I think he met a strange hermit outside town who taught him.}}",

        "\n"

        "\nI'm not sure where you'd find him, my best guess would be "
        "near the woods.}}"

        "\n\n{{gb:Press Enter to continue, or ask Clara more questions "
        "using}} {{lb:echo}}{{gb:.}}"
    ]

    def __init__(self, user_replies, xp=""):
        pass

    def check_command(self, current_dir):
        if self.last_user_input == "echo 2":
            text = (
                "\n{{yb:How did you lock the protected-section}}"
                "\n\nClara: {{Bb:I didn't! The only person that could do that "
                "was lead librarian."

                "\nHe had to find a special command to be able to do that. "
                "I think he met a strange hermit outside town who taught him.}}",

                "\n"

                "\nI'm not sure where you'd find him, my best guess would be "
                "near the woods.}}"

                "\n\n{{gb:Press Enter to continue, or ask Clara more questions "
                "using}} {{lb:echo}}{{gb:.}}"
            )
            self.send_text(text)
            self.level_passed = True

    def next(self):
        play_sound("bell")
        NextStep(self.xp)
'''
