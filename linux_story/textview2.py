#!/usr/bin/env python
"""Show a shell command's output in a gtk.TextView without freezing the UI"""

import os
import threading
import locale

import gobject
import gtk
import re
import time

#from helper_functions import typing_animation

gobject.threads_init()
gtk.gdk.threads_init()

encoding = locale.getpreferredencoding()
utf8conv = lambda x: unicode(x, encoding).encode('utf8')


def generate_tags(buffer):
    buffer.create_tag('orange_bg', background='orange')
    buffer.create_tag('yellow_bg', background='yellow')


def get_tag(buffer, tag_name):
    tag_table = buffer.get_tag_table()
    tag = tag_table.lookup(tag_name)
    return tag


def on_button_clicked(button, view, buffer, command):
    thr = threading.Thread(target=read_output, args=(view, buffer, command))
    thr.start()


def on_button_clicked2(button, view, buffer):
    thr = threading.Thread(target=read_output2, args=(view, buffer))
    thr.start()


def read_output(view, buffer, command):
    stdin, stdouterr = os.popen4(command)
    while 1:
        line = stdouterr.readline()
        if not line:
            break
        gtk.gdk.threads_enter()
        iter = buffer.get_end_iter()
        buffer.place_cursor(iter)
        buffer.insert(iter, utf8conv(line))
        view.scroll_to_mark(buffer.get_insert(), 0.1)
        gtk.gdk.threads_leave()


def read_output2(view, buffer):
    lines = typing_animation("hellooooooooooo")
    i = 0
    orange = get_tag(buffer, "orange_bg")

    for line in lines:
        i += 1
        gtk.gdk.threads_enter()

        iter = buffer.get_end_iter()
        buffer.place_cursor(iter)
        buffer.insert(iter, utf8conv(line))

        view.scroll_to_mark(buffer.get_insert(), 0.1)
        gtk.gdk.threads_leave()

        if i % 2 == 1:
            end_but_one_iter = buffer.get_end_iter()
            end_but_one_iter.backward_char()
            end_iter = buffer.get_end_iter()
            buffer.apply_tag(orange, end_but_one_iter, end_iter)

        time.sleep(0.1)

    #start_iter = buffer.get_start_iter()
    #end_iter = buffer.get_end_iter()
    #buffer.apply_tag(orange, start_iter, end_iter)


# Try spliting the words up into an array of groups of characters,
# that all need to get printed out one at a time
def typing_animation(string):
    rows, columns = os.popen('stty size', 'r').read().split()
    letters = []
    total_width = 0

    # First, process string.  Strip each character off unless it starts with \033
    # Then, strip it off in a chunk
    while len(string) != 0:

        if string.startswith('\033'):
            index2 = string.find('m')  # First time m comes up is directly after the selected number
            substring = string[0: index2 + 1]
            string = string[index2 + 1:]
            letters.append(substring)
            total_width += 1

        # If character is " ", see if we should replace it with a newline
        elif string.startswith(' '):
            # calculate distance to next line
            next_word = string.split(" ")[1]

            # remove all ansi escape sequences to find the real word length
            ansi_escape = re.compile(r'\x1b[^m]*m')
            clean_word = ansi_escape.sub('', next_word)
            next_word_len = len(clean_word)

            if total_width + next_word_len >= int(columns):
                total_width = 0
                letters.append('\n')
            else:
                total_width += 1
                letters.append(" ")
            string = string[1:]

        else:
            letters.append(string[0])
            string = string[1:]
            total_width += 1

    return letters


sw = gtk.ScrolledWindow()
sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
textview = gtk.TextView()
textbuffer = textview.get_buffer()
generate_tags(textbuffer)
sw.add(textview)
win = gtk.Window()
win.resize(300, 500)
win.connect('delete-event', gtk.main_quit)
button = gtk.Button(u"Press me!")
command = 'ls -R %s' % (os.getcwd(),)
button.connect("clicked", on_button_clicked2, textview, textbuffer)
vbox = gtk.VBox()
vbox.pack_start(button, False)
vbox.pack_start(sw)
win.add(vbox)
win.show_all()

gtk.main()
