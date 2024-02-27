import gi
import threading
import time
from datetime import datetime
from aboutlife.plugin import Plugin
from aboutlife.context import STATE
from aboutlife.overlay import client
from aboutlife.utils import send_notification, keygrab_loop

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import GObject, Gtk, GLib, Vte, Pango

GObject.type_register(Vte.Terminal)


class OverlayPlugin(Plugin):
    def __init__(self):
        self.tick: int = 0
        self.state: STATE = STATE.IDLE
        self.end_time: int = int(time.time())

        self.main_window = None
        self.notebook = None
        self.terminal = None
        self.tbx_task = None
        self.cbx_duration = None
        self.lbl_time = None
        self.lbl_waiting = None

    def setup(self):
        builder = Gtk.Builder()
        builder.add_from_file("aboutlife/overlay/ui.glade")
        builder.connect_signals(self)

        self.main_window = builder.get_object("main-window")
        self.main_window.connect("destroy", Gtk.main_quit)
        self.main_window.connect("show", self.reset)
        self.main_window.connect("delete-event", lambda x, y: True)

        self.notebook = builder.get_object("main-notebook")
        self.terminal = builder.get_object("terminal")
        self.tbx_task = builder.get_object("tbx-task")
        self.cbx_duration = builder.get_object("cbx-duration")
        self.lbl_time = builder.get_object("lbl-time")
        self.lbl_waiting = builder.get_object("lbl-waiting")
        # TODO: fallback font
        self.terminal.set_font(Pango.FontDescription("IosevkaTermNerdFontMono 12"))

        # signals
        button = builder.get_object("btn-close-tabs-1")
        button.connect("clicked", self.on_close_tabs)
        button = builder.get_object("btn-close-tabs-2")
        button.connect("clicked", self.on_close_tabs)
        button = builder.get_object("btn-tomato-1")
        button.connect("clicked", self.on_tomato_break)
        button = builder.get_object("btn-shutdown-1")
        button.connect("clicked", self.on_shutdown)
        button = builder.get_object("btn-shutdown-2")
        button.connect("clicked", self.on_shutdown)
        button = builder.get_object("btn-start-session")
        button.connect("clicked", self.on_start_session)
        button = builder.get_object("btn-duration-up")
        button.connect("clicked", lambda widget: self.on_spin_combobox(True))
        button = builder.get_object("btn-duration-down")
        button.connect("clicked", lambda widget: self.on_spin_combobox(False))

        # set high priority
        self.main_window.set_type_hint(Gtk.WindowType.POPUP)
        self.main_window.set_skip_taskbar_hint(True)
        self.main_window.set_skip_pager_hint(True)
        self.main_window.set_keep_above(True)
        self.main_window.set_decorated(False)
        self.main_window.present()
        self.main_window.stick()

        # grab keyboard
        thread = threading.Thread(target=keygrab_loop, args=(self.main_window,))
        thread.daemon = True
        thread.start()

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
        self.tick += 1
        if not self.main_window:
            return

        # each half a second
        if self.state == STATE.TOMATO_BREAK or self.state == STATE.OBLIGATORY_BREAK:
            now = int(time.time())
            if now <= self.end_time:
                sec = (self.end_time - now) % 60
                min = int((self.end_time - now - sec) / 60)
                text = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
                text = (
                    f"Tomato break {text}"
                    if self.state == STATE.TOMATO_BREAK
                    else f"Obligatory break {text}"
                )
                GLib.idle_add(self.lbl_waiting.set_text, text)
        else:
            GLib.idle_add(self.lbl_waiting.set_text, "")

        if self.tick % 2 == 0:  # each second
            pass
        if self.tick % 4 == 0:  # each two seconds
            print("D: stealing focus...")
            self.main_window.present()

            ctx = client.get_state()
            if not ctx:
                print("E: overlay process. couldn't connect to server")
                Gtk.main_quit()
                exit(1)
                return
            self.state = STATE(ctx.state)
            self.end_time = ctx.end_time

            if self.state == STATE.WORKING:
                print("I: overlay process. state changed to WORKING")
                Gtk.main_quit()
                exit(0)
                return

            text = datetime.now().strftime("%I:%M %p, %d of %B %Y")
            GLib.idle_add(self.lbl_time.set_text, text)

            if self.state == STATE.TOMATO_BREAK:
                GLib.idle_add(self.notebook.set_current_page, 2)
            else:
                GLib.idle_add(self.notebook.set_current_page, 1)

    def cleanup(self):
        Gtk.main_quit()

    def on_spin_combobox(self, up: bool):
        current = self.cbx_duration.get_active()
        desired = current - 1
        if up:
            desired = current + 1
        if desired < 0:
            return
        self.cbx_duration.set_active(desired)

    def on_tomato_break(self, widget):
        print("D: triggered 'tomato break'")
        success = client.put_start_tomato_break()
        send_notification(
            "Tomato break",
            "Sent successfully" if success else "Can't do that right now",
        )

    def on_shutdown(self, widget):
        print("D: triggered 'shutdown'")
        success = client.delete_shutdown_system()
        send_notification(
            "Shutdown", "Sent successfully" if success else "Can't do that right now"
        )

    def on_close_tabs(self, widget):
        print("D: triggered 'close tabs'")
        success = client.delete_close_tabs()
        send_notification(
            "Close tabs", "Sent successfully" if success else "Can't do that right now"
        )

    def on_start_session(self, widget):
        print("D: triggered 'start session'")
        success = False
        try:
            task_info = self.tbx_task.get_text()
            duration = int(self.cbx_duration.get_active_text())

            success = client.put_start_work_session(task_info, duration)
        except Exception as e:
            success = False
            print(e)
        send_notification(
            "Start Session",
            "Sent successfully" if success else "Can't do that right now",
        )


def loop(plugin):
    while True:
        time.sleep(0.5)
        plugin.process()
        print("D: tick (overlay)")


def main():
    plugin = OverlayPlugin()
    thread = threading.Thread(target=loop, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.setup()


if __name__ == "__main__":
    main()
