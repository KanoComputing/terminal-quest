# TerminalUi.py
#
# Copyright (C) 2014-2018 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Terminal Gtk emulator


import os

from gi import require_version
require_version('Gtk', '3.0')
require_version('Vte', '2.90')

from gi.repository import Vte, GLib, Gdk, Pango


class TerminalUi(Vte.Terminal):

    def __init__(self, width, height, dark=False):
        Vte.Terminal.__init__(self)
        self.__dark = dark

        self.fork_command_full(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None
        )

        # This prevents the user scrolling back through the history
        # self.set_scrollback_lines(0)
        self.set_size(width, height)
        self.__setup_appearance()

    def __setup_appearance(self):
        self.__apply_fg_and_bg_colours()
        self.set_margin_top(10)
        self.set_margin_left(10)
        self.set_margin_right(10)
        font_desc = Pango.FontDescription()
        font_desc.set_family("monospace")
        font_desc.set_size(13 * Pango.SCALE)
        self.set_font(font_desc)

    def __apply_fg_and_bg_colours(self):
        fg_color = Gdk.Color.parse("#ffffff")[1]
        bg_color = self.__get_bg_colour()
        self.set_colors(fg_color, bg_color, [])
        self.show_all()

    def __get_bg_colour(self):
        if self.__dark:
            return Gdk.Color.parse("#260000")[1]
        else:
            return Gdk.Color.parse("#262626")[1]

    def feed_child(self, command):
        Vte.Terminal.feed_child(self, command, len(command))

    def launch_command(self, command):
        command = "temp=$(tty) ; " + command + " > $temp | reset\n"
        self.feed_child(command)

    def set_dark_theme(self):
        self.__dark = True
        self.__apply_fg_and_bg_colours()

    def set_normal_theme(self):
        self.__dark = False
        self.__apply_fg_and_bg_colours()
