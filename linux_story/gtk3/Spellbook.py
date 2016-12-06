# Spellbook.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


import os
import sys

from gi.repository import Gtk, Gdk

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)

from linux_story.common import images_dir
from linux_story.helper_functions import get_ascii_art


class Spellbook(Gtk.EventBox):
    '''This is the GUI showing all the spells along the bottom
    '''

    SPELLBOOK_BORDER = 1
    SPELL_BORDER = 1
    CMD_HEIGHT = 80
    CMD_WIDTH = 80
    HEIGHT = 100
    number_of_spells = 10

    def __init__(self, is_caps_lock_on=False):
        self.stop = False
        self.is_caps_lock_on = is_caps_lock_on

        Gtk.EventBox.__init__(self)
        self.get_style_context().add_class("spellbook_background")

        self.box = Gtk.Box()
        self.grid = Gtk.Grid()
        self.caps_lock_warning = self.__create_caps_lock_warning()
        self.box.pack_start(self.grid, True, True, 0)
        self.box.pack_end(self.caps_lock_warning, False, False, 0)
        self.add(self.box)

        screen = Gdk.Screen.get_default()
        self.win_width = screen.get_width()
        self.win_height = screen.get_height()

        self.WIDTH = self.win_width / 2
        self.set_size_request(self.WIDTH, self.HEIGHT)

        self.__pack_locked_spells()

        # sigh.. this is basically to get showing and hiding right for the two widgets
        self.connect('show', self.__on_show)
        self.grid.connect('show', self.__on_show)
        self.caps_lock_warning.connect('show', self.__on_show)

    @staticmethod
    def __create_caps_lock_warning():
        box = Gtk.Box()
        box.get_style_context().add_class("caps_lock_warning")
        box.set_margin_top(10)
        box.set_margin_bottom(10)

        title = '<span foreground="orange" font="15" weight="bold">' \
                'Watch out, Caps Lock is activated on your keyboard' \
                '</span>'
        description = 'Terminal commands are \'case sensitive\' so have to be written' \
                      ' with capital or lower\ncase letters exactly as the computer' \
                      ' expects them, for example write' \
                      ' <span foreground="yellow">ls</span> not' \
                      ' <span foreground="yellow">LS</span>.'

        left_box = Gtk.Box()
        left_box.set_margin_left(10)
        left_box.add(Gtk.Image.new_from_file(os.path.join(images_dir, 'caps_lock.png')))

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_hexpand(True)
        right_box.set_margin_top(10)
        right_box.set_margin_bottom(10)
        right_box.set_margin_left(10)
        right_box.set_margin_right(10)

        title_label = Gtk.Label()
        title_label.set_markup(title)
        title_label.set_margin_bottom(3)
        title_label.set_halign(Gtk.Align.START)
        description_label = Gtk.Label()
        description_label.set_markup(description)
        right_box.add(title_label)
        right_box.add(description_label)

        box.add(left_box)
        box.add(right_box)

        return box

    def __on_show(self, widget):
        """
        Event handler for this widget on the 'show' event.
        """
        self.__show_or_hide_caps_lock_warning()

    def caps_lock_changed(self, is_caps_lock_on):
        """
        Update the CapsLock key status to show or hide the widget.

        This method gets called by the main_window.
        """
        self.is_caps_lock_on = is_caps_lock_on
        self.__show_or_hide_caps_lock_warning()

    def __show_or_hide_caps_lock_warning(self):
        """
        Show or hide the CapsLock notification widget instead of the spells
        depending on the key state.
        """
        if self.is_caps_lock_on:
            self.grid.hide()
            self.caps_lock_warning.show_all()
        else:
            self.grid.show_all()
            self.caps_lock_warning.hide()

    def repack_spells(self, commands, highlighted):
        '''
        Takes in the list of commands, and creates the spells and
        packs them into a grid.

        Args:
            commands (list): List of strings of the commands we want to show

        Returns:
            None
        '''

        left = 0

        for command in commands:
            if (left + 1) * (self.CMD_WIDTH + 20) < self.win_width:
                box = self.__create_spell(command, highlighted=command in highlighted)
                child = self.grid.get_child_at(left, 0)
                self.grid.remove(child)
                self.grid.attach(box, left, 0, 1, 1)
                left += 1

        self.__show_or_hide_caps_lock_warning()

    def __create_spell(self, name, locked=False, highlighted=False):
        '''
        Create the individual GUI for a spell.
        To create the icon, have the icon located at
        media/images/name.png

        Args:
            name (str): Name to be shown in the widget
            locked (bool): Whether we show the icon locked
                           i.e. with a padlock

        Returns:
            Gtk.Box: container widget for an individual spell
        '''

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_size_request(self.CMD_WIDTH, self.CMD_HEIGHT)
        box.set_margin_top(10)
        box.set_margin_left(10)
        box.set_margin_right(10)
        box.set_margin_bottom(10)

        icon_overlay = Gtk.Overlay()
        icon_overlay.set_size_request(80, 50)
        icon_overlay.set_opacity(0.99)
        if name != '...':
            icon_overlay.set_tooltip_markup(get_ascii_art(name + '_tooltip'))
        box.pack_start(icon_overlay, False, False, 0)

        icon_background = Gtk.EventBox()
        icon_background.get_style_context().add_class("spell_icon_background")
        icon_overlay.add(icon_background)

        label_background = Gtk.EventBox()
        label_background.get_style_context().add_class("spell_label_background")
        box.pack_start(label_background, False, False, 0)

        if locked:
            filename = os.path.join(images_dir, "padlock.png")
            icon_background.get_style_context().add_class("locked")
            label_background.get_style_context().add_class("locked")

        else:
            filename = os.path.join(images_dir, name + ".png")

            if highlighted:
                highlight_box = Gtk.EventBox()
                highlight_box.add(Gtk.Image.new_from_file(
                    os.path.join(images_dir, "overlay.gif")
                ))
                icon_background.add(highlight_box)

        icon_box = Gtk.EventBox()
        icon_box.add(Gtk.Image.new_from_file(filename))
        icon_overlay.add_overlay(icon_box)

        label = Gtk.Label(name)
        label.get_style_context().add_class("spell_command")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label_background.add(label)

        return box

    def __pack_locked_spells(self):
        '''
        Fill up the rest of the spellbook with locked boxes.
        '''

        left = 0

        while left < self.number_of_spells:
            locked_box = self.__create_spell("...", locked=True)
            self.grid.attach(locked_box, left, 0, 1, 1)
            left += 1

    def __set_theme(self):
        if self.dark:
            self.set_dark_theme()
        else:
            self.set_normal_theme()

    def set_dark_theme(self):
        style_context = self.get_style_context()
        if "dark" not in style_context.list_classes():
            self.get_style_context().add_class("dark")

    def set_normal_theme(self):
        style_context = self.get_style_context()
        if "dark" in style_context.list_classes():
            style_context.remove_class("dark")

