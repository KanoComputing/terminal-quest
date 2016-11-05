# dependencies.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This is where dependencies on external packages should go, to make it easier to create mocks for tests
# Also I hate having errors everywhere in my IDE, so this is my attempt to put them all in one place.

from gi.repository import Gtk, Gdk, Pango, GObject
from kano_profile.apps import load_app_state_variable as kp_load_app_state_variable
from kano_profile.apps import get_app_xp_for_challenge as kp_get_app_xp_for_challenge
from kano_profile.badges import save_app_state_variable_with_dialog as kp_save_app_state_variable_with_dialog
from kano.logging import logger as kp_logger
from kano.gtk3.apply_styles import apply_styling_to_screen as kano_apply_styling_to_screen
from kano.gtk3.scrolled_window import ScrolledWindow as Kano_ScrolledWindow
from kano_profile.tracker import Tracker as KpTracker
import kano_i18n.init


def install_i18n(name, path):
    return kano_i18n.init.install(name, path)


def load_app_state_variable(string1, string2):
    return kp_load_app_state_variable(string1, string2)


def get_app_xp_for_challenge(string1, string2):
    return kp_get_app_xp_for_challenge(string1, string2)


def save_app_state_variable_with_dialog(string1, string2, integer):
    return kp_save_app_state_variable_with_dialog(string1, string2, integer)


def translate(string):
    return _(string)


def apply_styling_to_screen(filename):
    return kano_apply_styling_to_screen(filename)


class Tracker(KpTracker):
    pass


class Logger:

    @staticmethod
    def debug(string):
        return kp_logger.debug(string)

    @staticmethod
    def error(string):
        return kp_logger.error(string)


class ScrolledWindow(Kano_ScrolledWindow):
    pass


class Window(Gtk.Window):
    pass


class Alignment(Gtk.Alignment):
    pass


class EventBox(Gtk.EventBox):
    pass


class Box(Gtk.Box):
    pass


class Label(Gtk.Label):
    pass


class Button(Gtk.Button):
    pass


class Grid(Gtk.Grid):
    pass


def vertical_orientation():
    return Gtk.Orientation.VERTICAL


def horizontal_orientation():
    return Gtk.Orientation.HORIZONTAL


SIGNAL_RUN_FIRST = GObject.SIGNAL_RUN_FIRST
