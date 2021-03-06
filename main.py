import game_of_life as gol
import gi
from webbrowser import open_new
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from gi.repository import Gio
import sys


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Game of life", application=app)
        self.set_default_size(500, 500)

        ### CONTAINER ###
        
        grid = Gtk.Grid()
        self.add(grid)

        self.game = gol.Grid(40)
        self.game.manualgen(gol.patterns.get('GGG'))

        ### ELEMENTS ###

        # Buttons
        self.reboot = Gtk.Button(label='Rb')
        self.reboot.connect('clicked', self.set_play)
        grid.attach(self.reboot,0,0,2,2)

        self.playpause = Gtk.Button(label='PP')
        self.playpause.connect('clicked', self.set_play)
        grid.attach(self.playpause,0,2,2,2)

        self.step = Gtk.Button(label='St')
        self.step.connect('clicked', self.set_play)
        grid.attach(self.step,0,4,2,2)

        self.save = Gtk.Button(label='Save')
        self.save.connect('clicked', self.set_play)
        grid.attach(self.save,2,0,1,1)

        self.ss = Gtk.Button(label='SS')
        self.ss.connect('clicked', self.set_play)
        grid.attach(self.ss,3,0,1,1)

        self.rand = Gtk.Button(label='Rand')
        self.rand.connect('clicked', self.set_play)
        grid.attach(self.rand,2,5,1,1)

        self.manual = Gtk.Button(label='Man')
        self.manual.connect('clicked', self.set_play)
        grid.attach(self.manual,3,5,1,1)

        self.nxn = Gtk.Button(label='Size')
        self.nxn.connect('clicked', self.set_play)
        grid.attach(self.nxn,2,1,2,1)

        self.velocity = Gtk.Button(label='Vel')
        self.velocity.connect('clicked', self.set_play)
        grid.attach(self.velocity,2,4,2,1)

        self.start = Gtk.Button(label='START')
        self.start.connect('clicked', self.startgame)
        grid.attach(self.start,2,2,2,2)

        ### ACTIONS ###

        # action without a state created (name, parameter type)
        copy_action = Gio.SimpleAction.new("copy", None)
        # connected with the callback function
        copy_action.connect("activate", self.copy_callback)
        # added to the window
        self.add_action(copy_action)

        # action without a state created (name, parameter type)
        paste_action = Gio.SimpleAction.new("paste", None)
        # connected with the callback function
        paste_action.connect("activate", self.paste_callback)
        # added to the window
        self.add_action(paste_action)

        # action with a state created (name, parameter type, initial state)
        shape_action = Gio.SimpleAction.new_stateful(
            "shape", GLib.VariantType.new('s'), GLib.Variant.new_string('line'))
        # connected to the callback function
        shape_action.connect("activate", self.shape_callback)
        # added to the window
        self.add_action(shape_action)

        # action with a state created
        about_action = Gio.SimpleAction.new("about", None)
        # action connected to the callback function
        about_action.connect("activate", self.about_callback)
        # action added to the application
        self.add_action(about_action)

        # action with a state created
        source_action = Gio.SimpleAction.new("source", None)
        # action connected to the callback function
        source_action.connect("activate", self.source_callback)
        # action added to the application
        self.add_action(source_action)

    def startgame(self, widget):
        self.game.animate('toroidal')

    def set_play(self, widget):
        if self.game.pause:
            self.game.pause = False
        else:
            self.game.pause = True
        print(self.game.pause)

    # callback function for copy_action
    def copy_callback(self, action, parameter):
        print("\"Copy\" activated")

    # callback function for paste_action
    def paste_callback(self, action, parameter):
        print("\"Paste\" activated")

    # callback function for shape_action
    def shape_callback(self, action, parameter):
        print("Shape is set to", parameter.get_string())
        # Note that we set the state of the action!
        action.set_state(parameter)

    def source_callback(self, action, parameter):
        open_new("https://github.com/AmadoCab/Proyecto2-progra")

    # callback function for about (see the AboutDialog example)
    def about_callback(self, action, parameter):
        # Instance of Gtk.AboutDialog
        aboutdialog = Gtk.AboutDialog()

        # Varibles of the aboutdialog
        image = GdkPixbuf.Pixbuf.new_from_file_at_scale('icono.png',4*12,5*12,True)
        authors = ["Amado Alberto Cabrera Estrada"]
        comments = "Implementación del juego de la vida de Conway para la clase de Programación matemática del segundo semestre de 2020."
        version = "1.0"

        # Fill the aboutdialog
        aboutdialog.set_logo(image)
        aboutdialog.set_program_name("Game of life")
        aboutdialog.set_copyright("Copyright \xc2\xa9 2020 Amado C.")
        aboutdialog.set_authors(authors)
        aboutdialog.set_comments(comments)
        aboutdialog.set_website("https://github.com/AmadoCab/Proyecto2-progra")
        aboutdialog.set_website_label("Github Source Code")
        aboutdialog.set_version(version)

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        aboutdialog.show()

    # a callback function to destroy the aboutdialog
    def on_close(self, action, parameter):
        action.destroy()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        # FIRST THING TO DO: do_startup()
        Gtk.Application.do_startup(self)

        # action without a state created
        new_action = Gio.SimpleAction.new("new", None)
        # action connected to the callback function
        new_action.connect("activate", self.new_callback)
        # action added to the application
        self.add_action(new_action)

        # action without a state created
        quit_action = Gio.SimpleAction.new("quit", None)
        # action connected to the callback function
        quit_action.connect("activate", self.quit_callback)
        # action added to the application
        self.add_action(quit_action)

        # action with a state created
        state_action = Gio.SimpleAction.new_stateful(
            "state",  GLib.VariantType.new('s'), GLib.Variant.new_string('off'))
        # action connected to the callback function
        state_action.connect("activate", self.state_callback)
        # action added to the application
        self.add_action(state_action)

        # action with a state created
        awesome_action = Gio.SimpleAction.new_stateful(
            "awesome", None, GLib.Variant.new_boolean(False))
        # action connected to the callback function
        awesome_action.connect("activate", self.awesome_callback)
        # action added to the application
        self.add_action(awesome_action)

        # a builder to add the UI designed with Glade to the grid:
        builder = Gtk.Builder()
        # get the file (if it is there)
        try:
            builder.add_from_file("menubar.xml")
        except:
            print("file not found")
            sys.exit()

        # we use the method Gtk.Application.set_menubar(menubar) to add the menubar
        # and the menu to the application (Note: NOT the window!)
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("appmenu"))

    # callback function for new
    def new_callback(self, action, parameter):
        print("You clicked \"New\"")

    # callback function for quit
    def quit_callback(self, action, parameter):
        print("You clicked \"Quit\"")
        sys.exit()

    # callback function for state
    def state_callback(self, action, parameter):
        print("State is set to", parameter.get_string())
        action.set_state(parameter)

    # callback function for awesome
    def awesome_callback(self, action, parameter):
        action.set_state(GLib.Variant.new_boolean(not action.get_state()))
        if action.get_state().get_boolean() is True:
            print("You checked \"Awesome\"")
        else:
            print("You unchecked \"Awesome\"")


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)