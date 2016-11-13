#
# bird.py
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A simple running bird animation for the init flow.
#
# TODO: Needs a LOT of refactoring.
#

import os
import sys
import time
import curses

import random

ASCII_RES_PATH = os.path.expanduser("~/weekend-work-2/terminal-Quest/linux_story/ascii_assets/story_files")

screen = None


def randint(a, b):
    if a >= b:
        return a
    else:
        return random.randint(a, b)

def draw_fn(y, x, msg, color=None):
    try:
        if color is None:
            screen.addstr(y, x, msg)
        else:
            screen.addstr(y, x, msg, color)
    except:
        shutdown_curses()
        raise


def load_animation(path):
    """
        Loads an ASCII art animation

        The animation must be stored in a plain text file
        frame-by-frame. Each frame must be delimited by
        a line consiting only of '---'.

        Example:

            FRAME1
            ---
            FRAME2
            ---
            FRAME3
            ---
    """

    frames = []
    with open(path) as f:
        frame = []
        for line in f:
            line = line.strip("\n")
            if line == "---":
                frames.append(frame)
                frame = []
            else:
                frame.append(line)

        # Append the last frame
        if len(frame) > 0:
            frames.append(frame)

    return frames


def animation_width(animation):
    """ Determine the maximum frame width of an animation """

    width = 0
    for frame in animation:
        for line in frame:
            if len(line) > width:
                width = len(line)

    return width


def animation_height(animation):
    """ Determine the maximum frame height of an animation """

    height = 0
    for frame in animation:
        if len(frame) > height:
            height = len(frame)

    return height


def debug(msg):
    log = 'curses-log'
    with open(log, 'a') as f:
        f.write(str(msg) + '\n')



def draw_frame(frame, x, y, animation_width):
    """
        Draw a sigle frame to a curses screen

        The frame is drawn from the [x,y] coordinates.
    """

    h, w = screen.getmaxyx()

    left_clip = 0
    if x < 0:
        left_clip = abs(x)
        x = 0

    right_clip = 0
    if (x + animation_width) >= w:
        right_clip = (x + animation_width) - w
        if right_clip > animation_width:
            right_clip = animation_width

    n = 0
    for line in frame:
        clipped_line = line[left_clip:(animation_width - right_clip)]
        if len(clipped_line) > 0:
            draw_fn(y + n, x, clipped_line)
            n += 1

def rabbit_lr():
    pass

def rabbit_rl():
    pass

def main(max_cycles, start_direction):
    # preload all parts of the animation
    ascii_lr = load_animation(ASCII_RES_PATH + "/bird-animation")
    ascii_w = animation_width(ascii_lr)
    ascii_h = animation_height(ascii_lr)

    # reverse this if needs be
    ascii_rl = load_animation(ASCII_RES_PATH + "/bird-animation")

    h, w = screen.getmaxyx()

    if h < 18:
        return


    # screen centre
    cx, cy = w/2, h/2


    if start_direction == "left-to-right":
        startx = -ascii_w
        rabbit = ascii_lr
        offset_diff = 10
    else:
        startx = w
        rabbit = ascii_rl
        offset_diff = -10

    starty = randint(0, h - ascii_h - 1)

    frame = 0
    cycle = 0
    offsetx = offsety = 0
    while True:
        n = 0
        while n < ascii_h:
            draw_fn(starty + n, 0, " "*(w))
            n += 1

        draw_frame(rabbit[frame], startx + offsetx, starty, ascii_w)
        frame += 1
        if frame >= len(rabbit):
            frame = 0

        offsetx += offset_diff

        if max_cycles == 0 and startx + offsetx >= (cx - ascii_w/2):
            time.sleep(0.5)
            break
        # invert the direction lr -> rl
        elif startx + offsetx > w:
            rabbit = ascii_rl
            offset_diff = -offset_diff
            starty = randint(0, h - ascii_h - 1)
            cycle += 1
            if cycle >= max_cycles:
                break
        # invert the direction rl -> lr
        elif startx + offsetx < -ascii_w:
            rabbit = ascii_lr
            offset_diff = -offset_diff
            starty = randint(0, h - ascii_h - 1)
            cycle += 1
            if cycle >= max_cycles:
                break

        screen.refresh()

        time.sleep(0.15)

    return 0


def init_curses():
    global screen

    screen = curses.initscr()
    screen.clear()
    screen.refresh()
    curses.noecho()
    curses.cbreak()
    screen.keypad(1)
    curses.curs_set(0)

    curses.start_color()
    if curses.has_colors():
        curses.use_default_colors()


def shutdown_curses():
    curses.curs_set(2)
    screen.keypad(0)
    screen.clear()
    screen.refresh()
    curses.echo()
    curses.nocbreak()
    curses.endwin()


def rabbit(cycles=1, start_direction='left-to-right'):
    status = 1

    try:
        init_curses()
        status = main(cycles, start_direction)
    finally:
        shutdown_curses()

    return status


if __name__ == "__main__":
    max_cycles = 3
    if len(sys.argv) > 1:
        max_cycles = int(sys.argv[1])

    start_direction = "left-to-right"
    if len(sys.argv) > 2 and sys.argv[2] == "right-to-left":
        start_direction = "right-to-left"

    sys.exit(rabbit(max_cycles, start_direction))
