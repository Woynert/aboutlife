from aboutlife.plugin import Plugin
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
        # end button
        item_end = Gtk.MenuItem(label="Terminar")
        item_end.connect("activate", Gtk.main_quit)
        self.menu.append(item_end)
        # interrupt button
        item_interrupt = Gtk.MenuItem(label="Interrumpir")
        item_interrupt.connect("activate", Gtk.main_quit)
        self.menu.append(item_interrupt)
        self.menu.show_all()

        self.tray_icon.set_tooltip_text("Está bien :)")
        self.tray_icon.set_visible(True)
        self.tray_icon.connect("popup-menu", self.open_menu)
        Gtk.main()

    def process(self):
        pass

    def cleanup(self):
        Gtk.main_quit()

    def health_check(self):
        pass

    def open_menu(self, status_icon, button, time):
        self.menu.popup(None, None, None, status_icon, button, time)


if __name__ == "__main__":
    app = TrayPlugin()
    app.setup()
