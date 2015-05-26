#!/usr/bin/env python

# menu_screen.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows the menu for selecting the appropriate challenge

import os
from gi.repository import Gtk, GObject


# This doesn't include the introduction as the introduction isn't a challenge
chapters = {
    1: {
        'start_challenge': 1,
        'end_challenge': 9,
        'title': 'Start exploring'
    },
    2: {
        'start_challenge': 10,
        'end_challenge': 16,
        'title': 'Save a family'
    },
    3: {
        'start_challenge': 17,
        'end_challenge': 22,
        'title': 'Go to the farm'
    }
}


# Contains the text describing the challenges
challenges = {
    1: {
        'title': 'Wake up!'
    },
    2: {
        'title': 'Look in your wardrobe'
    },
    3: {
        'title': 'Look on your shelves'
    },
    4: {
        'title': 'Find Mum'
    },
    5: {
        'title': 'Where\'s Dad?'
    },
    6: {
        'title': 'Visit the town'
    },
    7: {
        'title': 'Town meeting'
    },
    8: {
        'title': 'The bell strikes'
    },
    9: {
        'title': 'Where\'s Mum?'
    },
    10: {
        'title': 'See more clearly'
    },
    11: {
        'title': 'Save the girl'
    },
    12: {
        'title': 'Save the dog'
    },
    13: {
        'title': 'Food hunt'
    },
    14: {
        'title': 'Folderton Hero'
    },
    15: {
        'title': 'Have a closer look'
    },
    16: {
        'title': 'A gift'
    },
    17: {
        'title': ''
    },
    18: {
        'title': ''
    },
    19: {
        'title': ''
    },
    20: {
        'title': ''
    },
    21: {
        'title': ''
    },
    22: {
        'title': ''
    },
    23: {
        'title': ''
    }
}


class MenuScreen(Gtk.EventBox):

    __gsignals__ = {
        # This returns an integer of the challenge the user wants to start from
        'challenge_selected': (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        Gtk.EventBox.__init__(self)
        grid = self.create_chapter_menu()
        self.add(grid)

    def show_challenge_menu_wrapper(self, widget, challenge_number):
        self.show_challenge_menu(challenge_number)

    def show_challenge_menu(self, challenge_number):
        for child in self:
            self.remove(child)

        grid = self.create_challenge_menu(challenge_number)
        self.add(grid)
        self.show_all()

    def create_chapter_menu(self):
        grid = Gtk.Grid()
        num_of_chapters = len(chapters)

        row = 0
        column = 0
        total_columns = 6

        for i in range(1, num_of_chapters + 1):
            button = self.create_chapter_button(i)
            grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        return grid

    def create_challenge_menu(self, chapter_number):

        grid = Gtk.Grid()
        start_challenge = chapters[chapter_number]['start_challenge']
        end_challenge = chapters[chapter_number]['end_challenge']

        row = 0
        column = 0
        total_columns = 6

        for i in range(start_challenge, end_challenge + 1):
            button = self.create_challenge_button(i)
            grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        return grid

    def create_challenge_button(self, challenge_number):
        button = Gtk.Button(challenge_number)
        button.connect("clicked", self.launch_challenge, challenge_number)

        title = challenges[challenge_number]['title']
        button.set_property('has-tooltip', True)
        button.connect('query-tooltip', self.custom_tooltip, title)
        return button

    def custom_tooltip(self, x, y, z, a, tooltip, title):
        '''There is a much simpler function for having a tooltip with just
        text, but if we want to make it more complex, we can just modify this
        widget here.
        '''
        # Edit this if we want the tooltip to get any more complicated.
        custom_widget = Gtk.Label(title)
        tooltip.set_custom(custom_widget)
        return True

    def create_chapter_button(self, chapter_number):
        button = Gtk.Button(chapter_number)
        button.connect(
            "clicked", self.show_challenge_menu_wrapper, chapter_number
        )
        return button

    def launch_challenge(self, widget, challenge_number):
        self.emit('challenge_selected', challenge_number)

    # Currently not used, as linux-story-gui should have been launched by the
    # time you inialise this class.
    def directly_launch_challenge(self, challenge_number):
        # We want to launch either the local linux-story-gui or the system one,
        # depending on where this file is.
        # If this starts with /usr/ go to /usr/bin, otherwise use a relative
        # path.
        if os.path.dirname(__file__).startswith('/usr'):
            filepath = '/usr/bin/linux-story-gui'
        else:
            filepath = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../bin/linux-story-gui"
                )
            )

        command = (
            "python " +
            filepath + " " +
            str(challenge_number) + " 1"
        )

        os.system(command)


class TestWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect('delete-event', Gtk.main_quit)
        menu = MenuScreen()
        self.add(menu)
        self.show_all()


if __name__ == '__main__':
    TestWindow()
    Gtk.main()
