# Storybook.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#


import time
import string as s
import os

from gi.repository import Gtk, Pango, Gdk

from kano.utils import has_min_performance, RPI_2_B_SCORE

from linux_story.sound_manager import SoundManager
from linux_story.helper_functions import get_ascii_art


if has_min_performance(RPI_2_B_SCORE):
    NEWLINE_SLEEP = 0.15
    OTHER_SLEEP = 0.025
else:
    NEWLINE_SLEEP = 0.07
    OTHER_SLEEP = 0.007


class Storybook(Gtk.TextView):
    '''
    This class displays all the hints and description text for the user
    on the left side of the application.
    '''

    def __init__(self, width, height):
        Gtk.TextView.__init__(self)
        self.__generate_tags()

        # Remove the right click pop up
        self.connect("button-press-event", self.prevent_right_click)

        self.width = width
        self.height = height

        self.set_size_request(self.width, height)
        font_desc = Pango.FontDescription()
        font_desc.set_family("monospace")
        font_desc.set_size(13*Pango.SCALE)
        self.override_font(font_desc)
        self.get_style_context().add_class("storybook_background")
        self.char_width = self.__get_char_width()
        self.set_can_focus(False)
        self.language = self.__get_language()

        self.sounds_manager = SoundManager()

        self.set_margin_top(10)
        self.set_margin_left(10)
        self.set_margin_right(10)

        self.set_normal_theme()

    def set_dark_theme(self):
        style_context = self.get_style_context()
        if "dark" not in style_context.list_classes():
            self.get_style_context().add_class("dark")
            self.get_style_context().remove_class("normal")

    def set_normal_theme(self):
        style_context = self.get_style_context()
        if "dark" in style_context.list_classes():
            self.get_style_context().remove_class("dark")
            self.get_style_context().add_class("normal")
            self.show_all()

    def clear(self):
        '''Clear all text in spellbook
        '''
        self.get_buffer().set_text('', 0)

    def type_coloured_text(self, string):
        """
        Adds colour to the string and prints string with a typing effect.

        Args:
            string (str): Text we want to print with a typing effect

        Returns:
            None
        """
        lines = self.__parse_string(string)
        unstyled_string = self.__compose_string(lines)

        for i in xrange(len(lines)):
            line = lines[i]

            # if we are printing a new word, notify the sound manager
            if i == 0:
                self.sounds_manager.on_typing_story_text(unstyled_string)
            else:
                if unstyled_string[i - 1] in s.whitespace and \
                   unstyled_string[i] in s.letters:

                    self.sounds_manager.on_typing_story_text(unstyled_string[i:])

            self.__style_char(
                line['letter'],

                # TODO: get size tag working
                [line['colour'], line['bold']]
            )
            if line['letter'] == '\n':
                time.sleep(NEWLINE_SLEEP)
            else:
                time.sleep(OTHER_SLEEP)

            # tell GTK to flush the textbuffer and refresh the textview
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

    def print_coloured_text(self, string):
        '''
        Adds colours to the string and prints the coloured output.
        Same as self.type_coloured_text but without the sleeps between
        printing individual letters.

        Args:
            string (str): Text we want to print to the TextView

        Returns:
            None
        '''

        lines = self.__parse_string(string)

        for line in lines:
            self.__style_char(
                line['letter'],

                # TODO: get size tag working
                [line['colour'], line['bold']]
            )

    def __style_char(self, line, tag_names):
        '''
        Add styling (e.g. colours) to each character and puts it into the
        text buffer

        Args:
            line (str):
            tag_names :
        '''

        textbuffer = self.get_buffer()
        insert_iter = textbuffer.get_end_iter()
        textbuffer.place_cursor(insert_iter)

        # Inserts character into text buffer here
        # textbuffer.insert(line) also works
        textbuffer.insert_at_cursor(line)

        self.scroll_to_mark(textbuffer.get_insert(), 0.1, False, 0, 0)

        textbuffer = self.get_buffer()
        end_but_one_iter = textbuffer.get_end_iter()
        end_but_one_iter.backward_char()
        end_iter = textbuffer.get_end_iter()

        for tag_name in tag_names:
            tag = self.__get_tag(tag_name)
            textbuffer.apply_tag(tag, end_but_one_iter, end_iter)

    def print_challenge_title(self, challenge_number="1"):
        '''
        Print Challenge title from file at the top of the Story widget

        Args:
            challenge_number (str): e.g. "1"

        Returns:
            None
        '''

        if challenge_number == "0":
            text = _("INTRODUCTION\n")
        else:
            text = _("CHALLENGE {}\n").format(challenge_number)

        border = "-------------------\n"
        header = "\n" + border + "\n" + text + "\n" + border
        self.print_text(header)

    def print_text(self, string):
        '''
        Mimic for python print function
        '''

        # To mimic print function
        string = string + '\n'
        textbuffer = self.get_buffer()
        end_iter = textbuffer.get_end_iter()
        white_tag = self.__get_tag('white')
        textbuffer.insert_with_tags(end_iter, string, white_tag)

    def print_coming_soon(self, window, terminal):
        self.__print_text_banner("coming_soon")

    def print_finished(self, window, terminal):
        self.__print_text_banner("finished_terminal_quest")

    def __print_text_banner(self, filename):
        text = get_ascii_art(filename)
        text_lines = text.splitlines()
        leading_newlines = len(text_lines)
        for i in xrange(leading_newlines, -1, -1):
            self.clear()

            for j in xrange(i):
                self.print_text('')

            for j in xrange(leading_newlines - i):
                self.print_text(text_lines[j])

            time.sleep(0.2)

            # tell GTK to flush the textbuffer and refresh the textview
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

    def __generate_tags(self):
        '''
        Generate tags and adds them to the text buffer
        '''
        textbuffer = self.get_buffer()
        textbuffer.create_tag('orange_bg', background='orange')
        textbuffer.create_tag('white', foreground='white')
        textbuffer.create_tag('yellow_bg', background='yellow')

        textbuffer.create_tag('light_green', foreground="#D6FC49")
        textbuffer.create_tag('blue', foreground='#559bea')
        textbuffer.create_tag('lilac', foreground='#AAA7FA')
        textbuffer.create_tag('green', foreground='#7DCF02')
        textbuffer.create_tag('cyan', foreground='#00FFEE')
        textbuffer.create_tag('light_blue', foreground='#a2eabf')
        textbuffer.create_tag('purple', foreground='#c894f1')
        textbuffer.create_tag('pink', foreground="#EB98D2")
        textbuffer.create_tag('red', foreground='#D94C4A')
        textbuffer.create_tag('orange', foreground='#ff842A')
        textbuffer.create_tag('yellow', foreground='#FFE229')

        textbuffer.create_tag('bold', weight=Pango.Weight.BOLD)
        textbuffer.create_tag('not-bold', weight=Pango.Weight.NORMAL)
        textbuffer.create_tag('small', size=0)
        textbuffer.create_tag('medium', size=5)
        textbuffer.create_tag('large', size=10)

    def __get_tag(self, tag_name):
        '''
        Args:
            tag_name (str): id for the tag wanted.

        Returns:
            Gtk.TextTag
        '''

        textbuffer = self.get_buffer()
        tag_table = textbuffer.get_tag_table()
        tag = tag_table.lookup(tag_name)
        return tag

    def __split_into_lines(self, string):
        '''Adds new line characters appropriately into the string
        so the text wraps around correctly.
        This takes into account when the string is of the form
        "{{wb:hello}} {{rb:world}}", which means the curly brackets disappear
        when the text is typed to the console.

        Args:
            string (str)
        Returns:
            str: with newline characters inserted.
        '''

        columns = self.width / self.char_width
        total_width = 0
        new_string = ''

        # If character is ' ', see if we should replace it with a newline
        while len(string) != 0:

            if string[0] == ' ':
                # calculate distance to next line
                next_word = string.split(' ')[1]

                # if coloured
                index = next_word.find('{{')
                while index != -1:
                    next_word = next_word.replace(
                        next_word[index: index + 3],
                        ''
                    )
                    index = next_word.find('{{')

                index = next_word.find('}}')

                while index != -1:
                    next_word = next_word.replace(
                        next_word[index: index + 2],
                        ''
                    )
                    index = next_word.find('}}')

                next_word_len = len(next_word)

                if total_width + next_word_len >= int(columns):
                    total_width = 0
                    new_string = new_string + '\n'
                    string = string[1:]
                else:
                    total_width += 1
                    new_string = new_string + string[0]
                    string = string[1:]

            elif string[:2] == '{{':

                # Normally the string is of the form
                # "{{wb:blah blah}}"
                # need to cut out the part from the {{ to the :
                colon_index = string.find(":")

                # This should always be satisfied.
                if not colon_index == -1:
                    # This is so we don't include the colon when we
                    # are slicing the strings.
                    colon_index += 1
                    new_string = new_string + string[:colon_index]
                    string = string[colon_index:]
                else:
                    new_string = new_string + string[:3]
                    string = string[3:]
            elif string[:2] == '}}':
                new_string = new_string + string[:2]
                string = string[2:]
            elif string[0] == '\n':
                total_width = 0
                new_string = new_string + string[0]
                string = string[1:]
            else:
                total_width += 1
                new_string = new_string + string[0]
                string = string[1:]

        return new_string

    def __split_into_lines_nospace(self, string):
        '''Adds new line characters appropriately into the string
        so the text wraps around correctly, for languages which do
        not have spaces between words (like Japanese).

        Args:
            string (str)
        Returns:
            str: with newline characters inserted.
        '''

        total_width = 0
        new_string = ''

        while len(string) != 0:

            if string[:2] == '{{':
                # Normally the string is of the form
                # "{{wb:blah blah}}"
                # need to cut out the part from the {{ to the :
                colon_index = string.find(":")

                # This should always be satified.
                if not colon_index == -1:
                    # This is so we don't include the colon when we
                    # are slicing the strings.
                    colon_index += 1
                    new_string = new_string + string[:colon_index]
                    string = string[colon_index:]
                else:
                    new_string = new_string + string[:3]
                    string = string[3:]
            elif string[:2] == '}}':
                new_string = new_string + string[:2]
                string = string[2:]
            elif string[0] == '\n':
                total_width = 0
                new_string = new_string + string[0]
                string = string[1:]
            else:
                total_width += self.__get_width_of_char(string[0])
                margin = 20
                if total_width >= self.width - margin:
                    total_width = 0
                    new_string = new_string + '\n'
                else:
                    new_string = new_string + string[0]
                    string = string[1:]

        return new_string

    def __get_colour_from_id(self, colour_id='w'):
        """Look up what letter corresponds to what colour
        """

        pairs = {
            'r': 'red',
            'g': 'green',
            'G': 'light_green',
            'b': 'blue',
            'y': 'yellow',
            'o': 'orange',
            'w': 'white',
            'l': 'lilac',
            'c': 'cyan',
            'p': 'purple',
            'P': 'pink',
            'B': 'light_blue'
        }
        return pairs[colour_id]

    def __get_bold_from_id(self, bold_id='n'):
        '''Look up bold status from ID
        '''

        pairs = {
            'b': 'bold',
            'n': 'not-bold'
        }
        return pairs[bold_id]

    def __get_size_from_id(self, size_id='m'):
        '''Look up size from ID
        '''

        pairs = {
            's': 'small',
            'm': 'medium',
            'l': 'large'
        }
        return pairs[size_id]

    def __string_to_tag_list(self, string, colour, bold, size):
        '''
        Args:
            string (str): The text you want to appear in the Storybook
                          e.g. "he"
            colour (str): The colour the text should appear in
                          out of the tag list
            bold (str): Either 'bold' or 'not-bold'
            size (int): Currently this functionality is not working

        Returns:
            list: of the form [{'letter': 'h', 'colour': 'white', 'bold': 'bold'},
                               {'letter': 'e', 'colour': 'white', 'bold': 'bold'}]
        '''

        array = []
        for char in string:
            pair = {
                'letter': char,
                'colour': colour,
                'bold': bold,
                'size': size
            }
            array.append(pair)
        return array

    def __parse_string(self, string):
        '''
        Args:
            string (str): Of the form "{{wbs:hello this is a}} {{r:string}}"

        Returns:
            list: of the form [{'letter': 'h', 'colour': 'white', 'bold': 'bold'},
                               {'letter': 'e', 'colour': 'white', 'bold': 'bold'},
                               ...]
        '''

        # Get defaults
        default_colour = self.__get_colour_from_id()
        default_bold = self.__get_bold_from_id()
        default_size = self.__get_size_from_id()

        # Initialise changed variables
        colour = default_colour
        bold = default_bold
        size = default_size

        string_array = []
        if self.__is_space_delimited_lang():
            string = self.__split_into_lines(string)
        else:
            string = self.__split_into_lines_nospace(string)

        if string.find("{{") == -1:
            string_array = self.__string_to_tag_list(
                string,
                default_colour,
                default_bold,
                default_size
            )
            return string_array

        # First part of the string
        while string.find("{{") != -1:
            pos1 = string.index("{{")
            # Find the colon directly after the {{
            pos2 = string.find(":", pos1)

            # This gives the characters between the '{{' and '('.
            # These decide the tags we apply to the subsequent string
            attr = string[pos1 + 2:pos2]

            if len(attr) > 0:
                colour_id = attr[0]
                colour = self.__get_colour_from_id(colour_id)

            if len(attr) > 1:
                bold_id = attr[1]
                bold = self.__get_bold_from_id(bold_id)

            if len(attr) > 2:
                size_id = attr[2]
                size = self.__get_size_from_id(size_id)

            # {{ ?
            first_part = string[:pos1]

            # Last part of the string
            pos3 = string.index("}}")

            last_part = string[pos3 + 2:]

            # Colour part of the string
            colour_part = string[pos2 + 1:pos3]

            colour_part = self.__string_to_tag_list(
                colour_part,
                colour,
                bold,
                size
            )

            first_part = self.__string_to_tag_list(
                first_part,
                default_colour,
                default_bold,
                default_size
            )

            if last_part.find("{{") == -1:
                last_part = self.__string_to_tag_list(
                    last_part,
                    default_colour,
                    default_bold,
                    default_size
                )
                string_array = (
                    string_array + first_part + colour_part + last_part
                )
                string = ''
            else:
                string_array = string_array + first_part + colour_part
                string = last_part

        return string_array

    def __compose_string(self, lines):
        """
        Composes a parsed string from the string_array back together.

        Returns:
            unstyled_string (str): a single string without the custom markup symbols
        """
        unstyled_string = ''

        for line in lines:
            unstyled_string += line['letter']

        return unstyled_string

    def __get_char_width(self):
        '''
        Returns:
            int: the width of the letter 'a' in monospace font
        '''

        return self.__get_width_of_char('a')

    def __get_width_of_char(self, stringtomeasure):
        '''
        Returns:
            int: the width of some text in monospace font
        '''

        font_descr = Pango.FontDescription.new()
        font_descr.set_family('monospace')
        context = self.get_pango_context()
        layout = Pango.Layout.new(context)
        layout.set_font_description(font_descr)
        layout.set_text(stringtomeasure, -1)
        width, height = layout.get_pixel_size()
        #print "width: %d\n" % width

        return width

    def prevent_right_click(self, widget, event):
        '''
        Args:
            widget: Gtk.Widget
            event: Gdk.EventButton

        Returns:
            bool: True if the button clicked is the right button,
                  False otherwise
        '''

        # Detect if the event is a right click
        if event.button == 3:
            # If so, stop the event propagating to showing a right click menu
            return True

        return False

    def __get_language(self):
        '''
        Returns:
            str: the 2-letter language code (default: 'en')
        '''

        return os.environ.get('LANG', 'en').split('_')[0].lower()

    def __is_space_delimited_lang(self):
        '''
        Returns:
            bool: true if the current language has space-delimited words
        '''
        nospace_langs = ['ja']

        return self.language not in nospace_langs


