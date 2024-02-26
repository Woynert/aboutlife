import gi
import threading
import time
from aboutlife.plugin import Plugin
from aboutlife.context import STATE
from aboutlife.overlay import client

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import GObject, Gtk, GLib, Vte, Pango

GObject.type_register(Vte.Terminal)


class OverlayPlugin(Plugin):
    def __init__(self):
        self.main_window = None
        self.terminal = None
        self.tbx_task = None
        self.cbx_duration = None

    def setup(self):
        builder = Gtk.Builder()
        builder.add_from_file("aboutlife/overlay/ui.glade")
        builder.connect_signals(self)

        self.main_window = builder.get_object("main-window")
        self.main_window.connect("destroy", on_destroy)
        self.main_window.connect("show", self.reset)
        # self.main_window.connect("delete-event", lambda x, y: True)

        self.terminal = builder.get_object("terminal")
        self.tbx_task = builder.get_object("tbx-task")
        self.cbx_duration = builder.get_object("cbx-duration")
        # TODO: fallback font
        self.terminal.set_font(Pango.FontDescription("IosevkaTermNerdFontMono 12"))

        # signals
        button = builder.get_object("btn-close-tabs-1")
        button.connect("clicked", self.on_close_tabs)
        button = builder.get_object("btn-close-tabs-2")
        button.connect("clicked", self.on_close_tabs)
        button = builder.get_object("btn-tomato-1")
        button.connect("clicked", self.on_tomato_break)
        button = builder.get_object("btn-tomato-2")
        button.connect("clicked", self.on_tomato_break)
        button = builder.get_object("btn-shutdown-1")
        button.connect("clicked", self.on_shutdown)
        button = builder.get_object("btn-shutdown-2")
        button.connect("clicked", self.on_shutdown)
        button = builder.get_object("btn-start-session")
        button.connect("clicked", self.on_start_session)

        # set high priority
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

    def reset(self, widget):
        print("D: Starting setting up terminal")
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            None,
            ["/bin/vim", "/tmp/mimumi"],
            None,
            GLib.SpawnFlags.DEFAULT,
        )
        print("D: Done setting up terminal")

    def process(self):
        if not self.main_window:
            return

        print("D: stealing focus...")
        # self.main_window.present()

        # get current state

        context = client.get_state()
        if not context:
            return

        if context.state == STATE.WORKING.value:
            Gtk.main_quit()
            exit(0)

    def health_check(self):
        pass

    def cleanup():
        Gtk.main_quit()

    def on_tomato_break(self, widget):
        print("D: triggered 'tomato break'")
        success = client.put_start_tomato_break()
        print(success)
        pass

    def on_shutdown(self, widget):
        print("D: triggered 'shutdown'")
        success = client.delete_shutdown_system()
        print(success)
        pass

    def on_close_tabs(self, widget):
        print("D: triggered 'close tabs'")
        success = client.delete_close_tabs()
        print(success)
        pass

    def on_start_session(self, widget):
        print("D: triggered 'start session'")
        try:
            task_info = self.tbx_task.get_text()
            duration = int(self.cbx_duration.get_active_text())

            success = client.put_start_work_session(task_info, duration)
            print(success)
        except Exception as e:
            print(e)


def on_destroy(event):
    Gtk.main_quit()
    return True


def loop(plugin):
    while True:
        time.sleep(2)
        plugin.process()
        print("D: tick")


def main():
    plugin = OverlayPlugin()
    thread = threading.Thread(target=loop, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.setup()


if __name__ == "__main__":
    main()
