import game_of_life
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_default_size(500,500)

        # Container
        grid = Gtk.Grid()
        self.add(grid)

        # Botón
        b1 = Gtk.Button(label='Nada')
        b1.connect('clicked', self.on_button_clicked)
        grid.add(b1)

    def on_button_clicked(self, widget):
        print("Hello World")


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()