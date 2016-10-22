# TownPerson.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Only handles the behaviour of the NPC on the story side. Does not handle position of the character in the filesystem.


class TownPerson():
    # Add a source file for the ascii art?
    def __init__(self, responses):
        self.__responses = responses

    def speak(self, command):
        if command in self.__responses:
            return self.__responses[command]