import gi
import threading
import time
from aboutlife.plugin import Plugin

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class OverlayPlugin(Plugin):
    def __init__(self):
        self.main_window = None

    def setup(self):
        builder = Gtk.Builder()
        builder.add_from_file("aboutlife/overlay/ui.glade")
        builder.connect_signals(self)

        self.main_window = builder.get_object("main_window")
        self.main_window.connect("destroy", Gtk.main_quit)

        self.button = builder.get_object("button")
        self.button.connect("clicked", lambda x: print("Hello"))

        # take priority
        self.main_window.set_type_hint(Gtk.WindowType.POPUP)
        self.main_window.set_skip_taskbar_hint(True)
        self.main_window.set_skip_pager_hint(True)
        self.main_window.set_keep_above(True)
        self.main_window.set_decorated(False)
        self.main_window.present()
        self.main_window.stick()

        # start
        self.main_window.show_all()
        Gtk.main()

    def process(self):
        if not self.main_window:
            return

        # steal focus
        # TODO: while state != work
        print("D: stealing focus...")
        self.main_window.present()

    def health_check(self):
        pass

    def cleanup():
        Gtk.main_quit()


def thread_helper(plugin):
    while True:
        plugin.process()
        time.sleep(2)


if __name__ == "__main__":
    plugin = OverlayPlugin()
    thread = threading.Thread(target=thread_helper, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.setup()
