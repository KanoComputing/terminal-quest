import os
import sys


dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if __name__ == '__main__' and __package__ is None:
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


import pygcurse
import os


# This is the view
class TerminalWindow():
    def __init__(self):
        self._width = 100
        self._height = 100
        self._win = pygcurse.PygcurseWindow(self._width, self._height)
        self._location = ""
        self.set_fgcolor("white")

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    # This might be an internal function only
    def _set_location(self, location):
        # not sure if this is needed
        self._location = os.path.normpath(location)

    def set_fgcolor(self, color):
        self._win.fgcolor = color

    def set_prompt(self, location):
        self._set_location(location)
        self.set_fgcolor("yellow")
        username = os.environ['LOGNAME']
        self._win.write("{}@kano".format(username))
        self.set_fgcolor("blue")
        self._win.write(" {} $ ".format(self._location))
        self.set_fgcolor("white")

    def write_text(self, text):
        self._win.write(text)
        self.show()

    def show(self):
        self._win.update()

    def input(self):
        return self._win.raw_input()

    @property
    def cursor(self):
        return self._win.cursor

    def set_cursor(self, x, y):
        self._win.cursor = (x, y)

    def clear_line(self, x, y):
        '''
        y gives the position of the line to be cleared
        '''
        self._win.fill(
            ' ',
            fgcolor='white',
            bgcolor='black',
            region=(x, y, self.width, 1)
        )
