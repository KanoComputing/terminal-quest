import gtk
import glib
import subprocess
from helper_functions import typing_animation


class CommandTextView(gtk.TextView):
    ''' NICE TEXTVIEW THAT READS THE OUTPUT OF A COMMAND SYNCRONOUSLY '''
    def __init__(self):
        '''COMMAND : THE SHELL COMMAND TO SPAWN'''
        super(CommandTextView, self).__init__()
        self.set_editable(False)

    def run_command(self, command):
        ''' RUNS THE PROCESS '''
        args = command.split(' ')
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)  # SPAWNING
        glib.io_add_watch(proc.stdout,  # FILE DESCRIPTOR
                          glib.IO_IN,  # CONDITION
                          self.write_to_buffer)  # CALLBACK

    def write_to_buffer(self, fd, condition):
        if condition == glib.IO_IN:  # IF THERE'S SOMETHING INTERESTING TO READ
            char = fd.read(1)  # WE READ ONE BYTE PER TIME, TO AVOID BLOCKING
            buf = self.get_buffer()
            buf.insert_at_cursor(char)  # WHEN RUNNING DON'T TOUCH THE TEXTVIEW!!
            return True  # FUNDAMENTAL, OTHERWISE THE CALLBACK ISN'T RECALLED
        else:
            return False  # RAISED AN ERROR: EXIT AND I DON'T WANT TO SEE YOU ANYMORE


# TEST DRIVEN DEVELOPEMENT, WRITE THE TEST:
def test():
    ctv = CommandTextView()
    win = gtk.Window()
    win.connect("delete-event", lambda wid, event: gtk.main_quit())  # DEFINING CALLBACKS WITH LAMBDAS
    win.set_size_request(200, 300)
    win.add(ctv)
    win.show_all()
    ctv.run_command("ls -l")
    gtk.main()


if __name__ == '__main__':
    test()
