#!/usr/bin/env python

# menu_screen.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Shows the menu for selecting the appropriate challenge

import os
import sys

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from gi.repository import Gtk, GObject
from linux_story.common import get_max_challenge_number
from kano_profile.apps import load_app_state_variable
from linux_story.titles import challenges, chapters


'''

TITLE

MENU BUTTONS

INFO BOX

'''


class MenuScreen(Gtk.Alignment):
    '''This shows the user the challenges they can select.
    '''

    __gsignals__ = {
        # This returns an integer of the challenge the user wants to start from
        'challenge_selected': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'chapter_highlighted': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'challenge_highlighted': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }

    width = 500
    height = 200

    def __init__(self):
        Gtk.Alignment.__init__(
            self, xalign=0.5, yalign=0.5, xscale=0, yscale=0
        )

        self.background = Gtk.EventBox()
        self.background.get_style_context().add_class("menu_background")
        self.background.set_size_request(self.width, self.height)

        self.add(self.background)

        # Find the greatest challenge that has been created according to
        # kano profile
        self.max_challenge = get_max_challenge_number()

        # Get the last unlocked challenge.
        self.last_unlocked_challenge = load_app_state_variable(
            'linux-story', 'level'
        )

        if self.last_unlocked_challenge:
            # With this data, we need to decide which chapters are locked.
            self.last_unlocked_chapter = challenges[self.last_unlocked_challenge]['chapter']
            self.continue_story_or_select_chapter_menu()

        else:
            self.directly_launch_challenge(1)

    def update_descriptions(self, title, description):
        self.menu_title.set_text(title)
        self.menu_description.set_text(description)

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
        label.set_padding(10, 10)
        return label

    def continue_story_or_select_chapter_menu(self, widget=None):
        '''This gives the user a simple option of just continuing the story
        from where they left off, or selecting the chapter manually
        '''

        grid = Gtk.Grid()
        grid.set_row_spacing(8)
        grid.set_column_spacing(8)
        label = self.create_menu_title("TERMINAL QUEST")

        # This takes the user to the latest point in the story
        continue_btn = self.create_menu_button("CONTINUE")

        # For now, remove the launching functionality.
        continue_btn.connect(
            "clicked", self.launch_challenge, self.last_unlocked_challenge
        )

        # This takes the user to the chapter menu
        select_chapter_btn = self.create_menu_button("SELECT CHAPTER")
        select_chapter_btn.connect("clicked", self.show_chapter_menu_wrapper)

        grid.attach(label, 0, 0, 1, 1)
        grid.attach(continue_btn, 0, 1, 1, 1)
        grid.attach(select_chapter_btn, 0, 2, 1, 1)

        align = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        align.add(grid)

        self.replace_widget(align)

        # Make the CONTINUE button grab the focus
        continue_btn.grab_focus()
        self.show_all()

    ################################################################
    # Lots of repetition here.

    def show_challenge_menu_wrapper(self, widget, challenge_number):
        self.show_challenge_menu(challenge_number)

    def show_challenge_menu(self, challenge_number):
        '''Show a menu for the challenges available in a certain chapter
        '''

        self.menu = self.create_challenge_menu(challenge_number)
        self.replace_widget(self.menu)

        # Reset the highlighted location
        button = self.button_grid.get_child_at(0, 0)
        button.grab_focus()

        self.show_all()

    def show_chapter_menu_wrapper(self, widget):
        self.show_chapter_menu()

    def show_chapter_menu(self):
        self.menu = self.create_chapter_menu()
        self.replace_widget(self.menu)

        # Reset the highlighted location
        button = self.button_grid.get_child_at(0, 0)
        button.grab_focus()
        self.show_all()

    def create_generic_menu(self, title):
        '''Create a grid which we can then attach callbacks to the buttons
        '''
        label = self.create_menu_title(title)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)

        # Include back button
        self.back_btn = self.create_back_button()

        hbox = Gtk.Box(spacing=20)
        hbox.pack_start(self.back_btn, False, False, 0)
        hbox.pack_start(grid, False, False, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        # Pack into an alignment to centre the menu
        align = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        align.add(vbox)

        return (align, vbox, grid)

    def create_menu(self, title, start, end, create_button_cb, back_button_cb):
        '''Create a menu of the available chapters
        '''

        # hbox is the total container, grid is the container that has all
        # the buttons
        (align, box, grid) = self.create_generic_menu("CHAPTERS")
        self.button_grid = grid
        self.back_btn.connect(
            'clicked', back_button_cb
        )

        row = 0
        column = 0
        total_columns = 6

        for i in range(start, end + 1):
            button = create_button_cb(i)
            grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        # Show title and description
        self.info_box = self.create_info_box()

        # Pack the title and description in the menu
        box.pack_start(self.info_box, False, False, 10)

        return align

    def create_chapter_menu(self):
        '''Create a menu of the available chapters
        '''

        num_of_chapters = len(chapters)
        return self.create_menu(
            "CHAPTERS",
            1,
            num_of_chapters,
            self.create_chapter_button,
            self.continue_story_or_select_chapter_menu
        )

    def create_challenge_menu(self, chapter_number):

        start_challenge = chapters[chapter_number]['start_challenge']
        end_challenge = chapters[chapter_number]['end_challenge']

        return self.create_menu(
            "CHALLENGES",
            start_challenge,
            end_challenge,
            self.create_challenge_button,
            self.show_chapter_menu_wrapper
        )

    def create_menu_button(self, title):
        width = 50
        height = 50

        button = Gtk.Button(title)
        button.set_size_request(width, height)
        button.get_style_context().add_class("menu_button")
        return button

    def create_back_button(self):
        button = self.create_menu_button("<- BACK")
        # Get title, description.
        title = "Press ENTER to go to the previous screen"
        description = ""

        button.connect(
            "focus-in-event", self.edit_info_box_focus_in_wrapper,
            title, description
        )
        return button

    def create_menu_number_button(self, number, locking_number):
        button = self.create_menu_button(number)

        if number > locking_number:
            button.get_style_context().add_class("locked")
            button.set_sensitive(False)

        return button

    def create_challenge_button(self, number):
        button = self.create_menu_number_button(
            number, self.last_unlocked_challenge
        )

        # Get title, description from the yaml.
        title = challenges[number]["title"]
        # description = challenges[number]["description"]
        description = ""

        button.connect(
            "focus-in-event", self.edit_info_box_focus_in_wrapper, title,
            description
        )

        button.connect("clicked", self.launch_challenge, number)
        return button

    def create_chapter_button(self, number):
        button = self.create_menu_number_button(
            number, self.last_unlocked_chapter
        )

        # Get title, description from the yaml.
        title = chapters[number]["title"]
        # description = chapters[number]["description"]
        description = ""

        button.connect(
            "focus-in-event", self.edit_info_box_focus_in_wrapper, title,
            description
        )

        button.connect(
            "clicked", self.show_challenge_menu_wrapper, number
        )
        return button

    ####################################################################

    def create_info_box(self, title="", description=""):
        '''This shows the information about the chapter the user is trying
        to select.
        '''
        background = Gtk.EventBox()

        # width = 400
        # height = 50
        # background.set_size_request(width, height)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # These are the descriptions and titles for the menu
        self.menu_title = Gtk.Label(title)
        self.menu_title.get_style_context().add_class("menu_title")

        self.menu_description = Gtk.Label(description)
        self.menu_description.get_style_context().add_class("menu_description")

        box.pack_start(self.menu_title, False, False, 0)
        box.pack_start(self.menu_description, False, False, 0)

        background.add(box)

        # align = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        # align.add(box)
        # background.add(align)

        return background

    def edit_info_box_focus_in_wrapper(self, widget, event, title,
                                       description):
        self.edit_info_box(title, description)

    def edit_info_box(self, title, description):
        self.menu_title.set_text(title)
        self.menu_description.set_text(description)

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


if __name__ == "__main__":

    from linux_story.common import css_dir
    from kano.gtk3.apply_styles import apply_styling_to_screen

    window = Gtk.Window()

    # add styling
    CSS_FILE = os.path.join(
        css_dir,
        "style.css"
    )
    COLOUR_CSS_FILE = os.path.join(
        css_dir,
        "colours.css"
    )

    apply_styling_to_screen(CSS_FILE)
    apply_styling_to_screen(COLOUR_CSS_FILE)

    menuscreen = MenuScreen()
    window.add(menuscreen)
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()

    Gtk.main()
