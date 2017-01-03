from linux_story.story.tasks.Task import Task
from linux_story.gameobjects.TownPerson import TownPerson


class TalkToSwordsmaster(Task):

    def __init__(self):
        swordsmaster = TownPerson(
            {
                # I seek for a way to unlock the private section in the library
                "echo 1": _("\n{{wb:Swordsmaster:}} {{Bb:Child, why do you seek me?}}\"}}")
            }
        )
