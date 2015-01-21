

from gi.repository import Gtk, Gdk, Pango


class TextView(Gtk.TextView):

    def __init__(self):
        Gtk.TextView.__init__(self)
        print self.get_string_width()
        self.set_widget_width()

    def get_string_width(self):
        stringtomeasure = 'ohhoooollo'

        font_descr = Pango.FontDescription.new()
        font_descr.set_family('monospace')

        context = self.get_pango_context()

        layout = Pango.Layout.new(context)
        layout.set_font_description(font_descr)
        layout.set_text(stringtomeasure, -1)
        pixel_size = layout.get_pixel_size()
        return pixel_size

    def set_widget_width(self):
        screen = Gdk.Screen.get_default()
        width = 300
        print 'width = {}'.format(width)
        height = screen.get_height() - 200
        self.set_size_request(width, height)


if __name__ == '__main__':
    win = Gtk.Window()
    text_view = TextView()
    win.add(text_view)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
