import pygcurse
import os


# This is the view
class TerminalWindow():
    def __init__(self):
        self._win = pygcurse.PygcurseWindow(40, 25)
        self._location = ""
        self.set_fgcolor("white")

    # This might be an internal function only
    def _set_location(self, location):
        # not sure if this is needed
        self._location = location

    def set_fgcolor(self, color):
        self._win.fgcolor = color

    def set_prompt(self, location):
        self.set_fgcolor("yellow")
        username = os.environ['LOGNAME']
        self._win.write("{}@kano".format(username))
        self.set_fgcolor("blue")
        self._set_location(location)
        self._win.write(" {} $ ".format(location))
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
