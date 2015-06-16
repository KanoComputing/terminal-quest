#!/usr/bin/env python

# ColouredTextView.py
#
# Copyright (C) 2014 Kano Computing Ltd
# License: GNU General Public License v2 http://www.gnu.org/licenses/gpl-2.0.txt
#
# Author: Caroline Clark <caroline@kano.me>
# Print text in a TextView with a typing effect

import threading
import os
from gi.repository import Gtk, Pango, Gdk
import time
from kano.utils import is_model_2_b

if is_model_2_b():
    NEWLINE_SLEEP = 0.15
    OTHER_SLEEP = 0.025
else:
    NEWLINE_SLEEP = 0.07
    OTHER_SLEEP = 0.007


class Storybook(Gtk.TextView):

    def __init__(self, width=None, height=None):
        Gtk.TextView.__init__(self)
        self.__generate_tags()

        screen = Gdk.Screen.get_default()

        self.width = width
        self.height = height

        if not width:
            self.width = screen.get_width() / 2

        if not height:
            height = screen.get_height() - 300

        self.set_size_request(self.width, height)
        font_desc = Pango.FontDescription()
        font_desc.set_family("monospace")
        self.override_font(font_desc)
        bg_colour = Gdk.RGBA()
        bg_colour.parse("#313131")
        self.override_background_color(Gtk.StateFlags.NORMAL, bg_colour)
        self.char_width = self.__get_char_width()
        self.set_can_focus(False)

    def clear(self):
        '''Clear all text in spellbook
        '''
        self.get_buffer().set_text('', 0)

    def print_output(self, string):
        '''Prints string with a typing effect
        '''

        lines = self.__split_into_printable_chars(string)

        for line in lines:
            self.__style_char(
                line['letter'],

                # TODO: get size tag working
                [line['colour'], line['bold']]
            )

            if line['letter'] == '\n':
                time.sleep(NEWLINE_SLEEP)
            else:
                time.sleep(OTHER_SLEEP)

            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

    ##############################################################
    def print_coloured_output(self, string):
        # hacky function - same as above but removed the sleeps.
        lines = self.__split_into_printable_chars(string)

        for line in lines:
            self.__style_char(
                line['letter'],

                # TODO: get size tag working
                [line['colour'], line['bold']]
            )
    ##############################################################

    def __style_char(self, line, tag_names):
        '''Add styling (e.g. colours) to each character and puts it into the
        text buffer
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
        '''Print Challenge title from file at the top of the Story widget
        '''

        if challenge_number == "0":
            text = "INTRODUCTION\n"
        else:
            text = "CHALLENGE {}\n".format(challenge_number)

        border = "-------------------\n"
        header = "\n" + border + "\n" + text + "\n" + border
        self.print_text(header)

    def print_text(self, string):
        '''Mimic for python print function
        '''

        # To mimic print function
        string = string + '\n'
        textbuffer = self.get_buffer()
        end_iter = textbuffer.get_end_iter()
        white_tag = self.__get_tag('white')
        textbuffer.insert_with_tags(end_iter, string, white_tag)

    def __generate_tags(self):
        '''Generate tags and adds them to the text buffer
        '''

        green = Gdk.RGBA()
        green.parse('#7DCF02')
        lilac = Gdk.RGBA()
        lilac.parse('#AAA7FA')
        pink = Gdk.RGBA()
        pink.parse("#EB98D2")
        cyan = Gdk.RGBA()
        cyan.parse('#00FFEE')
        light_blue = Gdk.RGBA()
        light_blue.parse('#a2eabf')
        purple = Gdk.RGBA()
        purple.parse('#c894f1')
        red = Gdk.RGBA()
        # red.parse('#F52F11')
        red.parse('#D94C4A')
        orange = Gdk.RGBA()
        orange.parse('#EB6841')
        yellow = Gdk.RGBA()
        yellow.parse('#FFE229')

        textbuffer = self.get_buffer()
        textbuffer.create_tag('orange_bg', background='orange')
        textbuffer.create_tag('white', foreground='white')
        textbuffer.create_tag('yellow_bg', background='yellow')
        textbuffer.create_tag('blue', foreground='blue')

        textbuffer.create_tag('lilac', foreground_rgba=lilac)
        textbuffer.create_tag('green', foreground_rgba=green)
        textbuffer.create_tag('cyan', foreground_rgba=cyan)
        textbuffer.create_tag('light_blue', foreground_rgba=light_blue)
        textbuffer.create_tag('purple', foreground_rgba=purple)
        textbuffer.create_tag('pink', foreground_rgba=pink)
        textbuffer.create_tag('red', foreground_rgba=red)
        textbuffer.create_tag('orange', foreground_rgba=orange)
        textbuffer.create_tag('yellow', foreground_rgba=yellow)

        textbuffer.create_tag('bold', weight=Pango.Weight.BOLD)
        textbuffer.create_tag('not-bold', weight=Pango.Weight.NORMAL)
        textbuffer.create_tag('small', size=0)
        textbuffer.create_tag('medium', size=5)
        textbuffer.create_tag('large', size=10)

    def __get_tag(self, tag_name):
        '''Gets tag from tag table
        '''

        textbuffer = self.get_buffer()
        tag_table = textbuffer.get_tag_table()
        tag = tag_table.lookup(tag_name)
        return tag

    def __split_into_printable_chars(self, string):
        '''Try spliting the words up into an array of groups of characters,
        that all need to get printed out one at a time
        '''

        char_array = self.__parse_string(string)
        return char_array

    def __split_into_lines(self, string):
        '''Adds new line characters appropriately so the text wraps around
        correctly
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

    def __get_colour_from_id(self, colour_id='w'):
        '''Look up letter of colour
        '''

        pairs = {
            'r': 'red',
            'g': 'green',
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
        '''Look up bold status from ID
        '''

        pairs = {
            's': 'small',
            'm': 'medium',
            'l': 'large'
        }
        return pairs[size_id]

    def __string_to_tag_list(self, string, colour, bold, size):
        '''Turns string into an array of the form
        [{'letter': 'h', 'colour': 'white', 'bold': 'bold'},
         {'letter': 'e', 'colour': 'white', 'bold': 'bold'}]
        with the specified colours
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
        '''Change string of the form
        "{{wbs:hello this is a}} {{r:string}}"
        into an array of the form
        [{'letter': 'h', 'colour': 'white', 'bold': 'bold'},
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
        string = self.__split_into_lines(string)

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

    def __get_char_width(self):
        '''Get the character length in a monospaced font.
        This is useful so we can judge when we need to add newline characters
        '''

        stringtomeasure = 'a'
        font_descr = Pango.FontDescription.new()
        font_descr.set_family('monospace')
        context = self.get_pango_context()
        layout = Pango.Layout.new(context)
        layout.set_font_description(font_descr)
        layout.set_text(stringtomeasure, -1)
        width, height = layout.get_pixel_size()
        return width


# Test container for the Storybook widget
class Window(Gtk.Window):

    def __init__(self):
            Gtk.Window.__init__(self)
            self.set_size_request(500, 500)
            self.connect('delete-event', Gtk.main_quit)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.add(vbox)
            button = Gtk.Button("Click meeee")
            self.textview = Storybook()
            vbox.pack_start(self.textview, False, False, 0)
            vbox.pack_start(button, False, False, 0)
            button.connect("clicked", self.on_button_clicked)
            self.show_all()

    def on_button_clicked(self, button):
        array = [
            "Alarm : Beep beep beep! Beep beep beep!",
            "Radio : \"Good Morning, this is the 7am news.\"",
            "\"There have been reports of strange activity occurring in the "
            "town of Folderton today, as the number of reports of missing "
            "people and damaged buildings continues to increase...\"",
            "\"...nobody can explain what is causing the phenomenon, and "
            "Mayor Hubert has called an emergency town meeting...\"",
            "It's time to get up sleepy head!",
            "\n{{wNew Spell:}} {{yls}} - lets you see what's around you."
        ]
        string = '\n'.join(array)
        t = threading.Thread(target=self.textview.print_output, args=(string,))
        t.start()


if __name__ == "__main__":
    Window()
    Gtk.main()
