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
from gi.repository import Gtk, GObject, Pango, Gdk
import time

GObject.threads_init()


class Storybook(Gtk.TextView):

    def __init__(self):
        Gtk.TextView.__init__(self)
        self.__generate_tags()

        screen = Gdk.Screen.get_default()
        height = screen.get_height() - 300
        self.width = screen.get_width() / 2
        self.set_size_request(self.width, height)
        font_desc = Pango.FontDescription()
        font_desc.set_family("monospace")
        self.override_font(font_desc)
        black = Gdk.RGBA(0, 0, 0)
        self.override_background_color(Gtk.StateFlags.NORMAL, black)
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
            GObject.idle_add(
                self.__style_char,
                line['letter'],
                [line['color'], line['bold']]
            )
            if line['letter'] == '\n':
                time.sleep(0.07)
            else:
                time.sleep(0.04)

    def print_challenge_title(self, challenge_number="1"):
        '''Print Challenge title from file at the top of the Story widget
        '''

        fpath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../animation/" + challenge_number
        )
        with open(fpath) as f:
            for line in f.readlines():
                self.__print(line.rstrip())
        self.__print("")

    def __print(self, string):
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

        textbuffer = self.get_buffer()
        textbuffer.create_tag('orange_bg', background='orange')
        textbuffer.create_tag('orange', foreground='orange')
        textbuffer.create_tag('white', foreground='white')
        textbuffer.create_tag('yellow_bg', background='yellow')
        textbuffer.create_tag('yellow', foreground='yellow')
        textbuffer.create_tag('red', foreground='red')
        textbuffer.create_tag('blue', foreground='blue')
        textbuffer.create_tag('green', foreground='green')
        textbuffer.create_tag('bold', weight=Pango.Weight.BOLD)
        textbuffer.create_tag('not-bold', weight=Pango.Weight.NORMAL)

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

    def __get_color_from_id(self, color_id='w'):
        '''Look up letter of colour
        '''

        pairs = {
            'r': 'red',
            'g': 'green',
            'b': 'blue',
            'y': 'yellow',
            'o': 'orange',
            'w': 'white'
        }
        return pairs[color_id]

    def __string_to_color_list(self, string, color, bold='not-bold'):
        '''Turns string into array of the form
        [{'letter': 'h', 'color': 'white'}, {'letter': 'e', 'color': 'white'}]
        '''

        array = []
        for char in string:
            pair = {'letter': char, 'color': color, 'bold': bold}
            array.append(pair)
        return array

    def __parse_string(self, string):
        '''Change string of the form
        "{{whello this is a}} {{rstring}}"
        into an array of the form
        [{'letter': 'h', 'color': 'white'}, {'letter': 'e', 'color': 'white'}]
        '''

        default_color = self.__get_color_from_id()
        string_array = []
        string = self.__split_into_lines(string)
        if string.find("{{") == -1:
            string_array = self.__string_to_color_list(string, default_color)
            return string_array

        # First part of the string
        while string.find("{{") != -1:
            pos1 = string.index("{{")
            first_part = string[:pos1]
            # Last part of the string
            pos2 = string.index("}}")
            last_part = string[pos2 + 2:]
            # Preset id
            color_id = string[pos1 + 2]
            color = self.__get_color_from_id(color_id)
            # Color part of the string
            color_part = string[pos1 + 3:pos2]

            color_part = self.__string_to_color_list(color_part, color, 'bold')
            first_part = self.__string_to_color_list(first_part, default_color)

            if last_part.find("{{") == -1:
                last_part = self.__string_to_color_list(last_part, default_color)
                string_array = string_array + first_part + color_part + last_part
                string = ''
            else:
                string_array = string_array + first_part + color_part
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

    def __style_char(self, line, tag_names):
        '''Add styling (e.g. colours) to each character as it appears on the
        screen
        '''

        textbuffer = self.get_buffer()
        insert_iter = textbuffer.get_end_iter()
        textbuffer.place_cursor(insert_iter)
        textbuffer.insert(insert_iter, line)

        self.scroll_to_mark(textbuffer.get_insert(), 0.1, False, 0, 0)

        textbuffer = self.get_buffer()
        end_but_one_iter = textbuffer.get_end_iter()
        end_but_one_iter.backward_char()
        end_iter = textbuffer.get_end_iter()

        for tag_name in tag_names:
            tag = self.__get_tag(tag_name)
            textbuffer.apply_tag(tag, end_but_one_iter, end_iter)


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
        thr = threading.Thread(
            target=self.textview.print_output,
            args=[string]
        )
        thr.start()


if __name__ == "__main__":
    Window()
    Gtk.main()
