# Task.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This is the task that needs to be completed before the user can progress


class Task:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('Overwrite this function!')

    def get_hint_text(self, text):
        """
        :return: String: the hint that should be displayed to the screen
        """
        raise NotImplementedError('Overwrite this function!')

    def passed(self, text):
        """
        :return: bool - whether user should pass or not
        """
        raise NotImplementedError('Overwrite this function!')