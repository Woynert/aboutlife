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
ABOUT_TO_END_MINIMUM_SECS = 60

CSS = b"""
.window_alert {
  background-color: #bb0000;
  color: #ffffff;
  /* color: #e5a50a; */
}
.window_alert > frame > border {
  border-color: #440000;
}
"""


class StickyPlugin(Plugin):
    def __init__(self):
        # config
        self.discrete: bool = False

        # state
        self.tick: int = 0
        self.end_time: int = int(time.time())
        self.tick_last_shuffle: int = 0
        self.hidden: bool = True
        self.is_about_to_end: bool = False

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

        # register css
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # start
        self.window.show_all()
        self.shuffle_position()
        Gtk.main()

    def on_click(self, window, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
            self.shuffle_position()
            return True


    def update_label(self):
        if self.lbl_msg:
            text = ("🌀️ Objetivo: " + self.task_info if self.task_info != "" else
            ("Session ending soon..." if self.is_about_to_end else "Tiempo restante:"))

            GLib.idle_add(self.lbl_msg.set_text, text)


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
        self.update_label()

    def hide(self):
        if not self.window:
            return
        screen = self.window.get_screen()
        sw = screen.get_width()
        sh = screen.get_height()
        GLib.idle_add(self.window.move, sw, sh)

    def turn_red(self):
        ctx = self.window.get_style_context()
        ctx.add_class("window_alert")
        if self.lbl_time:
            self.lbl_time.set_visible(False)

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
        now = int(time.time())

        # Turn red if is_about_to_end.
        if (
            not self.is_about_to_end
            and (self.end_time - now) <= ABOUT_TO_END_MINIMUM_SECS
        ):
            self.is_about_to_end = True
            self.turn_red()

        # Shuffle.
        if (self.tick - self.tick_last_shuffle) >= SHUFFLE_DELAY:
            self.shuffle_position()

        # Force show if it's about to end.
        if self.is_about_to_end and self.hidden:
            self.hidden = False
            self.reset_shuffle_time()
            self.shuffle_position()

        # Hide after a while.
        if (
            self.discrete
            and not self.is_about_to_end
            and not self.hidden
            and (self.tick - self.tick_last_shuffle) >= DISCRETE_VISIBLE_DURATION
        ):
            self.hidden = True
            self.reset_shuffle_time()
            self.hide()

        # Every 2 secs: Update task info.
        if self.tick % 4 == 0:
            self.sync_state()
            self.update_label()

        # Evert half sec: Update timer label.
        if not self.hidden:
            if now <= self.end_time:
                sec = (self.end_time - now) % 60
                min = int((self.end_time - now - sec) / 60)
                text = f"{str(min).zfill(2)}:{str(sec).zfill(2)}"
                GLib.idle_add(self.lbl_time.set_text, text)

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
