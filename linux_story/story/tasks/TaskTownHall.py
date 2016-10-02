from linux_story.gameobjects.Npc import Npc
from linux_story.story.tasks.Task import Task


class TaskTownHall(Task):

    # noinspection PyMissingConstructor
    def __init__(self, *args, **kwargs):
        grumpy_man = Npc(
            {
                "cat grumpy-man": _("\n{{wb:Man:}} {{Bb:\"Help! I don't know what's happening to me. "
                                    "I heard this bell ring, and now my legs have gone all strange.\"}}")
            }
        )
        young_girl = Npc(
            {
                "cat young-girl": _("\n{{wb:Girl:}} {{Bb:\"Can you help me? I can't find my friend Amy anywhere. "
                                    "If you see her, will you let me know?\"}}")
            }
        )
        little_boy = Npc(
            {
                "cat little-boy": _("\n{{wb:Boy:}} {{Bb:\"Pongo? Pongo? Has anyone seen my dog Pongo? "
                                    "He's never run away before...\"}}")
            }
        )

        self.__characters = [grumpy_man, young_girl, little_boy]
        self.__command_tracker = {
            "cat grumpy-man", False,
            "cat young-girl", False,
            "cat little-boy", False
        }

    def passed(self, text):
        return self.get_hint_text(text) == ""

    def get_hint_text(self, text):
        if self.__number_of_characters_left() == 0:
            return ""

        if text == 'ls':
            return _("\n{{gb:You look around.}}")

        hint = self.__get_character_test(text)
        if hint:
            self.__command_tracker[text] = True
            return hint
        else:
            return _("{{rb:Use}} {{yb:%s}} {{rb:to progress.}}") % self.__command_tracker.keys()[0]

    def __number_of_characters_left(self):
        counter = len(self.__command_tracker)
        for character in self.__command_tracker:
            if self.__command_tracker[character]:
                counter -= 1

        return counter

    def __get_character_test(self, text):
        for character in self.__characters:
            response = character.speak(text)

            if response:
                response += self.__append_narrative_hint()
                return response

    def __append_narrative_hint(self):
        number = self.__number_of_characters_left()
        if number == 1:
            return _("\n{{gb:Well done! Check on 1 more person.}}\n")
        elif number > 0:
            return _("\n{{gb:Well done! Check on %d more people.}}\n") % number
        else:
            return _("\n{{gb:Press}} {{ob:Enter}} {{gb:to continue.}}")
