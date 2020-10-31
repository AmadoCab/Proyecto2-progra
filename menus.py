from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gio
import sys


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="MenuBar Example", application=app)
        self.set_default_size(200, 200)

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

    # callback function for about (see the AboutDialog example)
    def about_callback(self, action, parameter):
        # a  Gtk.AboutDialog
        aboutdialog = Gtk.AboutDialog()

        # lists of authors and documenters (will be used later)
        authors = ["GNOME Documentation Team"]
        documenters = ["GNOME Documentation Team"]

        # we fill in the aboutdialog
        aboutdialog.set_program_name("MenuBar Example")
        aboutdialog.set_copyright(
            "Copyright \xc2\xa9 2012 GNOME Documentation Team")
        aboutdialog.set_authors(authors)
        aboutdialog.set_documenters(documenters)
        aboutdialog.set_website("http://developer.gnome.org")
        aboutdialog.set_website_label("GNOME Developer Website")

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