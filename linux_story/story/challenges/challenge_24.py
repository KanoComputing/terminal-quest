#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# A chapter of the story

# Start of chapter 4


from linux_story.Step import Step
from linux_story.story.terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.challenges.challenge_25 import Step1 as NextChallengeStep


class StepTemplateMkdir(Step):
    challenge_number = 24

    def __init__(self, xp=''):
        Step.__init__(self, TerminalMkdir, xp)


class Step1(StepTemplateMkdir):
    story = [
        'Eleanor: {{Bb:I\'m so pleased you found me!  I was so scared '
        'when I heard the bell go off, I hid. But now I don\'t know where to go...}}',
        '{{Bb:My Mummy and Daddy have been taken by the bell...}}',
        '{{Bb:I want to see if we can help other people around town!}}',
        '{{Bb:Have you been to the suburbs in town?  We might find other '
        'people who know what\'s going on.',
        'I\'m not scared if I\'m with you!',
        'Head to town and I\'ll follow!'
    ]
    start_dir = "~/town/.hidden-shelter"
    end_dir = "~/town"

    def next(self):
        # Move Eleanor to "follow" the user
        Step2()


class Step2(StepTemplateMkdir):
    story = [
        'Eleanor: {{Bb:We\'re in the town square. Can we go to the suburbs?}}',
        '{{Bb:...do you not know where they are? They\'re right there.}}',
        '{{Bb:Look around to see.}}'
    ]

    start_dir = '~/town'
    end_dir = '~/town'

    def next(self):
        Step3()


class Step3(StepTemplateMkdir):
    story = [
        'Eleanor: {{Bb:See! There are the suburbs there. Did you not notice them before?}}',
        "{{Bb:Let's go there and see where we want to go}}"
    ]

    start_dir = "~/town"
    end_dir = "~/town/suburbs"

    def next(self):
        Step4()


class Step4(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:What's around?}}"
    ]

    start_dir = "~/town/suburbs"
    end_dir = "~/town/suburbs"

    def next(self):
        Step5()


class Step5(StepTemplateMkdir):
    story = [
        "Eleanor: {{Bb:Hey, what is that?}}",
        "{{lb:the-best-shed-maker-in-town}}?",
        "{{Bb: What's that? Let's go in!}}"
    ]

    start_dir = "town/suburbs"
    end_dir = "~/town/suburbs"

    def next(self):
        NextChallengeStep(self.xp)
