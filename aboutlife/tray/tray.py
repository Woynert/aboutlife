from aboutlife.plugin import Plugin
from aboutlife.context import Context
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TrayPlugin(Plugin):
    def __init__(self):
        self.tray_icon = None
        self.menu = None

    def setup(self):
        self.tray_icon = Gtk.StatusIcon()
        self.tray_icon.set_from_icon_name("avatar-default")
        self.tray_icon.connect("activate", lambda x: print("Hello"))

        self.menu = Gtk.Menu()
        item = Gtk.MenuItem(label="Terminar")
        item.connect("activate", self.on_finish)
        self.menu.append(item)
        self.menu.show_all()

        self.tray_icon.set_tooltip_text("Está bien :)")
        self.tray_icon.set_visible(True)
        self.tray_icon.connect("popup-menu", self.open_menu)
        Gtk.main()

    def process(self):
        pass

    def cleanup(self):
        Gtk.main_quit()

    def open_menu(self, status_icon, button, time):
        self.menu.popup(None, None, None, status_icon, button, time)

    def on_finish(self, widget):
        with Context.get_mutex():
            Context.get_singleton().setup_obligatory_break()


if __name__ == "__main__":
    app = TrayPlugin()
    app.setup()
