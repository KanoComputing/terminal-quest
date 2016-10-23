# MenuScreen.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Shows the menu for selecting the appropriate challenge


import os
import sys


if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../..'
        )
    )
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from linux_story.dependencies import translate, load_app_state_variable, Alignment, EventBox, Box, Label, Button, \
    vertical_orientation, Grid, SIGNAL_RUN_FIRST
from linux_story.common import get_max_challenge_number
from linux_story.titles import challenges, chapters


class MenuScreen(Alignment):
    '''This shows the user the challenges they can select.
    '''

    __gsignals__ = {
        # This returns an integer of the challenge the user wants to start from
        'challenge_selected': (SIGNAL_RUN_FIRST, None, (int,)),
        'chapter_highlighted': (SIGNAL_RUN_FIRST, None, (int,)),
        'challenge_highlighted': (SIGNAL_RUN_FIRST, None, (int,)),
    }

    width = 500
    height = 200

    def __init__(self):
        Alignment.__init__(self, xalign=0.5, yalign=0.5, xscale=0, yscale=0)

        self.background = EventBox()
        self.background.get_style_context().add_class("menu_background")
        self.background.set_size_request(self.width, self.height)

        self.add(self.background)

        # Find the greatest challenge that has been created according to
        # kano profile
        self.max_challenge = get_max_challenge_number()

        # Get the last unlocked challenge.
        self.last_unlocked_challenge = load_app_state_variable('linux-story', 'level')

        if self.last_unlocked_challenge:

            # If the last unlocked challenge is less than the max_challenge,
            # add one so the user can access the first locked-challenge.
            if self.last_unlocked_challenge < self.max_challenge:
                self.last_unlocked_challenge += 1

            # With this data, we need to decide which chapters are locked.
            self.last_unlocked_chapter = challenges[self.last_unlocked_challenge]['chapter']
            self.continue_story_or_select_chapter_menu()

    def continue_story_or_select_chapter_menu(self, widget=None):
        """This gives the user a simple option of just continuing the story
        from where they left off, or selecting the chapter manually.
        """

        vbox = Box(orientation=vertical_orientation())
        header = self.create_menu_header(
            translate("TERMINAL QUEST MENU"),
            translate("Use arrow keys to select the button")
        )

        # This takes the user to the latest point in the story
        continue_btn = self.create_menu_button(translate("CONTINUE STORY"))

        # For now, remove the launching functionality.
        continue_btn.connect(
            "clicked", self.launch_challenge, self.last_unlocked_challenge
        )

        # This takes the user to the chapter menu
        select_chapter_btn = self.create_menu_button(translate("SELECT CHAPTER"))
        select_chapter_btn.connect("clicked", self.show_chapter_menu_wrapper)

        vbox.pack_start(header, False, False, 15)
        vbox.pack_start(continue_btn, False, False, 0)
        vbox.pack_start(select_chapter_btn, False, False, 10)

        align = Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        align.add(vbox)
        align.set_padding(10, 10, 0, 0)

        self.replace_menu(align)

        # Make the CONTINUE button grab the focus
        continue_btn.grab_focus()
        self.show_all()

    def create_menu_title(self, title):
        label = Label(title)
        label.get_style_context().add_class('menu_title')

        return label

    def create_menu_description(self, description):
        label = Label(description)
        label.get_style_context().add_class('menu_description')
        return label

    def create_menu_header(self, title, description=""):
        vbox = Box(orientation=vertical_orientation())
        self.menu_title = self.create_menu_title(title)
        vbox.set_spacing(10)
        vbox.pack_start(self.menu_title, False, False, 0)

        if description:
            self.menu_description = self.create_menu_description(description)
            vbox.pack_start(self.menu_description, False, False, 0)

        return vbox

    def replace_menu(self, new_menu):
        """Unpack the widget in self.background, and
        pack the new widget in.
        """
        for child in self.background.get_children():
            self.background.remove(child)

        self.background.add(new_menu)
        self.show_all()

    ################################################################
    # Lots of repetition here.

    def show_challenge_menu_wrapper(self, widget, challenge_number):
        self.show_challenge_menu(challenge_number)

    def show_challenge_menu(self, challenge_number):
        """Show a menu for the challenges available in a certain chapter
        """

        self.menu = self.create_challenge_menu(challenge_number)
        self.replace_menu(self.menu)

        # Reset the highlighted location
        button = self.button_grid.get_child_at(0, 0)
        button.grab_focus()
        self.info_description.hide()

        self.show_all()

    def show_chapter_menu_wrapper(self, widget):
        self.show_chapter_menu()

    def show_chapter_menu(self):
        self.menu = self.create_chapter_menu()
        self.replace_menu(self.menu)

        # Reset the highlighted location
        button = self.button_grid.get_child_at(0, 0)
        button.grab_focus()
        self.show_all()

    def create_menu(self, title, start, end, create_button_cb, back_button_cb):
        """Create a menu of buttons
        """

        # hbox is the total container, grid is the container that has all
        # the buttons
        header = self.create_menu_header(title)

        self.button_grid = Grid()
        self.button_grid.set_row_spacing(10)
        self.button_grid.set_column_spacing(10)

        # Include back button
        self.back_btn = self.create_back_button()
        # self.button_grid.attach(self.back_btn, 0, 0, 1, 1)

        hbox = Box(spacing=20)
        hbox.pack_start(self.back_btn, False, False, 0)
        hbox.pack_start(self.button_grid, False, False, 0)

        # Align the grid
        grid_align = Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        grid_align.add(hbox)

        vbox = Box(orientation=vertical_orientation(), spacing=10)
        vbox.pack_start(header, False, False, 0)
        vbox.pack_start(grid_align, False, False, 0)

        # Pack into an alignment to centre the menu
        align = Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
        align.add(vbox)
        align.set_padding(10, 10, 0, 0)

        self.back_btn.connect('clicked', back_button_cb)

        row = 0
        column = 0
        total_columns = 6

        for i in range(start, end + 1):
            button = create_button_cb(i)
            self.button_grid.attach(button, column, row, 1, 1)
            column += 1

            if column > total_columns:
                row += 1
                column = 0

        # Show info title and info description of the relevent chapter
        # or challenge.
        self.info_box = self.create_info_box()

        # Pack the title and description in the menu
        vbox.pack_start(self.info_box, False, False, 10)

        return align

    def create_chapter_menu(self):
        """Create a menu of the available chapters
        """

        num_of_chapters = len(chapters)
        menu = self.create_menu(
            translate("CHAPTERS"),
            1,
            num_of_chapters,
            self.create_chapter_button,
            self.continue_story_or_select_chapter_menu
        )
        menu.set_margin_top(10)
        menu.set_margin_bottom(10)
        menu.set_margin_left(100)
        menu.set_margin_right(100)

        return menu

    def create_challenge_menu(self, chapter_number):

        start_challenge = chapters[chapter_number]['start_challenge']
        end_challenge = chapters[chapter_number]['end_challenge']

        menu = self.create_menu(
            translate("CHALLENGES"),
            start_challenge,
            end_challenge,
            self.create_challenge_button,
            self.show_chapter_menu_wrapper
        )
        menu.set_margin_top(10)
        menu.set_margin_bottom(10)
        menu.set_margin_left(10)
        menu.set_margin_right(10)

        return menu

    def create_menu_button(self, title):
        width = 50
        height = 50

        button = Button(title)
        button.set_size_request(width, height)
        button.get_style_context().add_class("menu_button")
        return button

    def create_back_button(self):
        button = self.create_menu_button(translate("<- BACK"))
        # Get title, description.
        title = translate("Press ENTER to go to the previous screen")
        description = ""

        button.connect(
            "focus-in-event", self.edit_info_box_wrapper, title,
            description
        )
        button.connect(
            "enter-notify-event", self.edit_info_box_wrapper, title,
            description
        )
        button.connect(
            "leave-notify-event", self.show_focused_button_info
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
        title = self.create_challenge_title(number)
        description = ""

        button.connect(
            "focus-in-event", self.edit_info_box_wrapper, title,
            description
        )
        button.connect(
            "enter-notify-event", self.edit_info_box_wrapper, title,
            description
        )

        button.connect(
            "leave-notify-event", self.show_focused_button_info
        )

        button.connect("clicked", self.launch_challenge, number)
        return button

    def create_challenge_title(self, number):
        return translate("Challenge {}: {}").format(number, challenges[number]["title"])

    def create_challenge_description(self, number):
        return

    def create_chapter_title(self, number):
        return translate("Chapter {}: {}").format(number, chapters[number]["title"])

    def create_chapter_description(self, number):
        return translate("Challenge {} to Challenge {}").format(
            chapters[number]["start_challenge"],
            chapters[number]["end_challenge"]
        )

    def create_chapter_button(self, number):
        button = self.create_menu_number_button(
            number, self.last_unlocked_chapter
        )

        # Get title, description from the yaml.
        title = self.create_chapter_title(number)
        description = self.create_chapter_description(number)

        button.connect(
            "focus-in-event", self.edit_info_box_wrapper, title,
            description
        )

        button.connect(
            "enter-notify-event", self.edit_info_box_wrapper, title,
            description
        )

        button.connect(
            "leave-notify-event", self.show_focused_button_info
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
        background = EventBox()
        background.set_size_request(450, 65)
        box = Box(orientation=vertical_orientation())
        box.set_spacing(5)

        # These are the descriptions and titles for the menu
        self.info_title = Label(title)
        self.info_title.get_style_context().add_class("info_title")
        box.pack_start(self.info_title, False, False, 0)

        self.info_description = Label(description)
        self.info_description.get_style_context().add_class("info_description")
        box.pack_start(self.info_description, False, False, 0)

        background.add(box)
        return background

    def edit_info_box_wrapper(self, widget, event, title, description):
        self.edit_info_box(title, description)

    def edit_info_box(self, title, description):
        self.info_title.set_text(title)
        if description:
            self.info_description.set_text(description)
            self.info_description.show()
        else:
            self.info_description.hide()

    def show_focused_button_info(self, *_):
        # Get the focused button in the button_grid
        for child in self.button_grid.get_children():
            if child.has_focus():

                # Get the label in button
                number = int(child.get_label())

                # Decide if we're showing the chapters or the challenges
                if self.menu_title.get_text() == translate("CHAPTERS"):
                    title = self.create_chapter_title(number)
                    description = self.create_chapter_description(number)
                else:
                    title = self.create_challenge_title(number)
                    description = self.create_challenge_description(number)

                self.edit_info_box(title, description)

    def launch_challenge(self, widget, challenge_number):
        self.emit('challenge_selected', challenge_number)
