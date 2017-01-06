#
# Animation.py
#
# Copyright (C) 2014-2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A simple running bird animation for terminal quest, heavily based on the rabbit animation.
#
#

import time
import curses
import random
import os
import sys
import struct

from linux_story.helper_functions import get_path_to_file_in_system


class Animation:
    def __init__(self, filename):
        self.__screen = None
        self.__path = get_path_to_file_in_system(filename)

    def play_across_screen(self, cycles=1, start_direction='left-to-right', speed=10):
        status = 1  # everything went wrong
        try:
            self.__init_curses()
            status = self.__run_animation_across_screen(cycles, start_direction, speed)
        except Exception as e:
            debug(str(e))
        finally:
            self.__shutdown_curses()

        return status

    def play_finite(self, cycles=1):
        status = 1  # everything went wrong
        try:
            self.__init_curses()
            status = self.__run_animation(cycles)
        except Exception as e:
            debug(str(e))
        finally:
            self.__shutdown_curses()

        return status

    def __init_curses(self):
        self.__screen = curses.initscr()
        self.__screen.clear()
        self.__screen.refresh()
        curses.noecho()
        curses.cbreak()
        self.__screen.keypad(1)
        curses.curs_set(0)

        curses.start_color()
        if curses.has_colors():
            curses.use_default_colors()

    def __shutdown_curses(self):
        curses.curs_set(2)
        self.__screen.keypad(0)
        self.__screen.clear()
        self.__screen.refresh()
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def __run_animation(self, max_cycles):
        ascii_frames = self.load_animation()
        ascii_w = animation_width(ascii_frames)
        ascii_h = animation_height(ascii_frames)
        w, h = get_width_height_of_terminal()

        if h < ascii_h or w < ascii_w:
            debug("The height of the terminal is too small for the animation")

        starty = startx = 0
        cycles = 0

        frame = 0
        offsetx = offsety = 0
        while True:
            n = 0
            while n < ascii_h:
                self.draw_fn(starty + n, 0, " " * (w))
                n += 1

            self.draw_frame(ascii_frames[frame], startx + offsetx, starty, ascii_w)
            frame += 1
            if frame >= len(ascii_frames):
                frame = 0
                cycles += 1
                if cycles == max_cycles:
                    break

            self.__screen.refresh()

            time.sleep(0.15)

        return 0


    def __run_animation_across_screen(self, max_cycles, start_direction, speed):
        # preload all parts of the animation
        ascii_lr = self.load_animation()
        ascii_w = animation_width(ascii_lr)
        ascii_h = animation_height(ascii_lr)

        # reverse this if needs be
        ascii_rl = self.load_animation()

        w, h = get_width_height_of_terminal()

        if h < ascii_h or w < ascii_w:
            debug("The height of the terminal is too small for the animation")

        # screen centre
        cx, cy = w / 2, h / 2

        if start_direction == "left-to-right":
            startx = -ascii_w
            rabbit = ascii_lr
            offset_diff = speed
        else:
            startx = w
            rabbit = ascii_rl
            offset_diff = -speed

        starty = randint(0, h - ascii_h - 1)

        frame = 0
        cycle = 0
        offsetx = offsety = 0
        while True:
            n = 0
            while n < ascii_h:
                self.draw_fn(starty + n, 0, " " * (w))
                n += 1

            self.draw_frame(rabbit[frame], startx + offsetx, starty, ascii_w)
            frame += 1
            if frame >= len(rabbit):
                frame = 0

            offsetx += offset_diff

            if max_cycles == 0 and startx + offsetx >= (cx - ascii_w / 2):
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

            self.__screen.refresh()

            time.sleep(0.15)

        return 0

    def load_animation(self):
        """
            Loads an ASCII art animation

            The animation must be stored in a plain text file
            frame-by-frame. Each frame must be delimited by
            a line consisting only of '---'.

            Example:

                FRAME1
                ---
                FRAME2
                ---
                FRAME3
                ---
        """

        frames = []
        with open(self.__path) as f:
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

    def draw_fn(self, y, x, msg, color=None):
        try:
            if color is None:
                self.__screen.addstr(y, x, msg)
            else:
                self.__screen.addstr(y, x, msg, color)
        except:
            self.__shutdown_curses()
            raise

    def draw_frame(self, frame, x, y, animation_width):
        """
            Draw a single frame to a curses screen

            The frame is drawn from the [x,y] coordinates.
        """

        w, h = get_width_height_of_terminal()

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
            self.draw_fn(y + n, x, clipped_line)
            n += 1


def get_width_height_of_terminal():
    """
    Originally retrieved from:
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python

    Curses.getmaxyx() did not pick up the correct width/height after resizing the terminal,
    and os.popen(stty size) did not work for all cases.
    """
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


def randint(a, b):
    if a >= b:
        return a
    else:
        return random.randint(a, b)


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
    log = os.path.join(os.path.expanduser("~"), 'curses-log')
    if not os.path.exists(log):
        open(log, "w+").close()

    with open(log, 'a') as f:
        f.write(str(msg) + '\n')


if __name__ == "__main__":
    Animation("firework-animation").play_finite(cycles=1)
