import gi
import threading
import time
from random import choice
from aboutlife.plugin import Plugin
from aboutlife.context import STATE
from aboutlife.overlay import client
from aboutlife.utils import get_resource_path

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

SCREEN_MARGIN = 60
TICK_DURATION = 0.5  # 1 tick = 1/2 seconds
SHUFFLE_DELAY = 60 * 1.5 * 2  # (ticks) 1.5 minutes
DISCRETE_VISIBLE_DURATION = 10 * 2  # (ticks) 15 seconds


class StickyPlugin(Plugin):
    def __init__(self):
        # config
        self.discrete: bool = False

        # state
        self.tick: int = 0
        self.end_time: int = int(time.time())
        self.tick_last_shuffle: int = 0
        self.hidden: bool = True

        # widgets
        self.pos_hori: int = 0
        self.pos_vert: int = 0
        self.window = None
        self.lbl_msg = None
        self.lbl_time = None

    def reset(self):
        self.pos_hori: int = 0
        self.pos_vert: int = 0
        self.window = None
        self.lbl_msg = None
        self.lbl_time = None

    def setup(self):
        builder = Gtk.Builder()
        builder.add_from_file(get_resource_path("/sticky/ui.glade"))
        builder.connect_signals(self)

        self.window = builder.get_object("main-window")
        self.lbl_msg = builder.get_object("lbl-msg")
        self.lbl_time = builder.get_object("lbl-time")
        self.window.connect("button-press-event", self.on_click)

        # set high priority
        self.window.set_type_hint(Gtk.WindowType.POPUP)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
        self.window.set_keep_above(True)
        self.window.set_decorated(False)
        self.window.stick()

        # prefer dark theme
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        # start
        self.window.show_all()
        self.shuffle_position()
        Gtk.main()

    def on_click(self, window, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self.shuffle_position()
            return True

    def reset_shuffle_time(self):
        self.tick_last_shuffle = self.tick

    def shuffle_position(self):
        if not self.window:
            return
        while True:
            hori = choice([-1, 0, 1])
            vert = choice([-1, 0, 1])
            if hori == 0 and vert == 0:
                vert = choice([-1, 1])
            if hori != self.pos_hori or vert != self.pos_vert:
                self.pos_hori = hori
                self.pos_vert = vert
                break

        self.reset_shuffle_time()
        screen = self.window.get_screen()
        sw = screen.get_width()
        sh = screen.get_height()
        ww = self.window.get_size()[0]
        wh = self.window.get_size()[1]
        x = self.pos_hori * (sw / 2 - ww / 2 - SCREEN_MARGIN) + sw / 2 - ww / 2
        y = self.pos_vert * (sh / 2 - wh / 2 - SCREEN_MARGIN) + sh / 2 - wh / 2
        GLib.idle_add(self.window.move, x, y)
        self.hidden = False

    def hide(self):
        if not self.window:
            return
        screen = self.window.get_screen()
        sw = screen.get_width()
        sh = screen.get_height()
        GLib.idle_add(self.window.move, sw, sh)

    def sync_state(self):
        ctx = client.get_state()
        if not ctx:
            print("E: sticky process. couldn't connect to server")
            Gtk.main_quit()
            exit(1)
            return

        if ctx.state != STATE.WORKING.value:
            print("I: sticky process. session over")
            Gtk.main_quit()
            exit(0)
            return

        self.discrete = ctx.sticky_discrete
        self.end_time = ctx.end_time
        self.task_info = ctx.task_info

    def process(self):
        self.tick += 1

        # each half a second
        if not self.hidden:
            now = int(time.time())
            if now <= self.end_time:
                sec = (self.end_time - now) % 60
                min = int((self.end_time - now - sec) / 60)
                text = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
                GLib.idle_add(self.lbl_time.set_text, text)

        if self.tick % 4 == 0:  # each two seconds
            self.sync_state()
            if self.lbl_msg:
                GLib.idle_add(self.lbl_msg.set_text, "🌀️ Objetivo: " + self.task_info)

        if (self.tick - self.tick_last_shuffle) >= SHUFFLE_DELAY:
            self.shuffle_position()

        if (
            self.discrete
            and not self.hidden
            and (self.tick - self.tick_last_shuffle) >= DISCRETE_VISIBLE_DURATION
        ):
            self.hidden = True
            self.reset_shuffle_time()
            self.hide()

    def cleanup(self):
        Gtk.main_quit()


def loop(plugin):
    while True:
        time.sleep(TICK_DURATION)
        plugin.process()


def main():
    plugin = StickyPlugin()
    thread = threading.Thread(target=loop, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.sync_state()
    plugin.setup()


if __name__ == "__main__":
    main()
