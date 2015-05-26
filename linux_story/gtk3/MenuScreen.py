#!/usr/bin/env python

# menu_screen.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows the menu for selecting the appropriate challenge

import os
from gi.repository import Gtk, GObject

from linux_story.common import get_max_challenge_number
from kano.gtk3.buttons import KanoButton
from kano_profile.apps import load_app_state_variable


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
        'title': 'Wake up!',
        'chapter': 1
    },
    2: {
        'title': 'Look in your wardrobe',
        'chapter': 1
    },
    3: {
        'title': 'Look on your shelves',
        'chapter': 1
    },
    4: {
        'title': 'Find Mum',
        'chapter': 1
    },
    5: {
        'title': 'Where\'s Dad?',
        'chapter': 1
    },
    6: {
        'title': 'Visit the town',
        'chapter': 1
    },
    7: {
        'title': 'Town meeting',
        'chapter': 1
    },
    8: {
        'title': 'The bell strikes',
        'chapter': 1
    },
    9: {
        'title': 'Where\'s Mum?',
        'chapter': 1
    },
    10: {
        'title': 'See more clearly',
        'chapter': 2
    },
    11: {
        'title': 'Save the girl',
        'chapter': 2
    },
    12: {
        'title': 'Save the dog',
        'chapter': 2
    },
    13: {
        'title': 'Food hunt',
        'chapter': 2
    },
    14: {
        'title': 'Folderton Hero',
        'chapter': 2
    },
    15: {
        'title': 'Have a closer look',
        'chapter': 2
    },
    16: {
        'title': 'A gift',
        'chapter': 2
    },
    17: {
        'title': '',
        'chapter': 3
    },
    18: {
        'title': '',
        'chapter': 3
    },
    19: {
        'title': '',
        'chapter': 3
    },
    20: {
        'title': '',
        'chapter': 3
    },
    21: {
        'title': '',
        'chapter': 3
    },
    22: {
        'title': '',
        'chapter': 3
    },
    23: {
        'title': '',
        'chapter': 3
    }
}


# TODO: have a design for the GUI.  For example, could have a terminal based
# selection screen
class MenuScreen(Gtk.Alignment):
    '''This shows the user the challenges they can select.
    '''

    __gsignals__ = {
        # This returns an integer of the challenge the user wants to start from
        'challenge_selected': (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        Gtk.Alignment.__init__(self, xalign=0.5, yalign=0.5, xscale=0, yscale=0)

        self.background = Gtk.EventBox()
        self.background.get_style_context().add_class("menu_background")

        self.add(self.background)
        self.set_size_request(300, 300)

        # Find the greatest challenge that has been created according to
        # kano profile
        self.max_challenge = get_max_challenge_number()

        # Get the last unlocked challenge.
        self.last_unlocked_challenge = load_app_state_variable('linux-story', 'level')

        # With this data, we need to decide which chapters are locked.
        self.last_unlocked_chapter = challenges[self.last_unlocked_challenge]['chapter']

        self.continue_story_or_select_chapter_menu()

    def replace_widget(self, new_menu):

        for child in self.background.get_children():
            self.background.remove(child)

        new_menu.set_margin_top(10)
        new_menu.set_margin_bottom(10)
        new_menu.set_margin_left(10)
        new_menu.set_margin_right(10)

        self.background.add(new_menu)
        self.show_all()

    def create_menu_title(self, title):
        label = Gtk.Label(title)
        label.get_style_context().add_class('menu_title')
        return label

    def continue_story_or_select_chapter_menu(self, widget=None):
        '''This gives the user a simple option of just continuing the story
        from where they left off, or selecting the chapter manually
        '''

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = self.create_menu_title("TERMINAL QUEST")

        # This takes the user to the latest point in the story
        continue_btn = KanoButton("CONTINUE")
        continue_btn.connect(
            'clicked', self.launch_challenge, self.last_unlocked_challenge
        )

        # This takes the user to the chapter menu
        select_chapter_btn = KanoButton('SELECT CHAPTER')
        select_chapter_btn.connect('clicked', self.show_chapter_menu_wrapper)

        vbox.pack_start(label, False, False, 5)
        vbox.pack_start(continue_btn, False, False, 0)
        vbox.pack_start(select_chapter_btn, False, False, 0)

        self.replace_widget(vbox)

    ################################################################
    # Lots of repetition here.

    def show_challenge_menu_wrapper(self, widget, challenge_number):
        self.show_challenge_menu(challenge_number)

    def show_challenge_menu(self, challenge_number):
        '''Show a menu for the challenges available in a certain chapter
        '''

        menu = self.create_challenge_menu(challenge_number)
        self.replace_widget(menu)

    def show_chapter_menu_wrapper(self, widget):
        self.show_chapter_menu()

    def show_chapter_menu(self):
        menu = self.create_chapter_menu()
        self.replace_widget(menu)
        self.show_all()

    def create_generic_menu(self, title):
        '''Create a grid which we can then attach callbacks to the buttons
        '''
        label = self.create_menu_title(title)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)

        # Include back button
        self.back_btn = KanoButton("<-", color='blue')

        hbox = Gtk.Box(spacing=20)
        hbox.pack_start(self.back_btn, False, False, 0)
        hbox.pack_start(grid, False, False, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        return (vbox, grid)

    def create_chapter_menu(self):
        '''Create a menu of the available chapters
        '''

        # hbox is the total container, grid is the container that has all
        # the buttons
        (box, grid) = self.create_generic_menu("CHAPTERS")
        num_of_chapters = len(chapters)
        self.back_btn.connect('clicked', self.continue_story_or_select_chapter_menu)

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

        return box

    def create_challenge_menu(self, chapter_number):
        (box, grid) = self.create_generic_menu("CHALLENGES")
        start_challenge = chapters[chapter_number]['start_challenge']
        end_challenge = chapters[chapter_number]['end_challenge']
        self.back_btn.connect('clicked', self.show_chapter_menu_wrapper)

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

        return box

    def create_challenge_button(self, challenge_number):
        button = KanoButton(challenge_number)
        button.connect("clicked", self.launch_challenge, challenge_number)

        title = challenges[challenge_number]['title']
        button.set_property('has-tooltip', True)
        button.connect('query-tooltip', self.custom_tooltip, title)

        # If the chapter number is greater than the maximum chapter unlocked,
        # set the styling to locked and make it insensitive.
        if challenge_number > self.last_unlocked_challenge:
            button.get_style_context().add_class("locked")
            button.set_sensitive(False)

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
        button = KanoButton(chapter_number)
        button.connect(
            "clicked", self.show_challenge_menu_wrapper, chapter_number
        )
        # If the chapter number is greater than the maximum chapter unlocked,
        # set the styling to locked and make it insensitive.
        if chapter_number > self.last_unlocked_chapter:
            button.get_style_context().add_class("locked")
            button.set_sensitive(False)

        return button

    ####################################################################

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
