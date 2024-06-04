import gi
import threading
import time
import os
from enum import Enum
from datetime import datetime
from aboutlife.plugin import Plugin
from aboutlife.context import STATE, TASK_MIN_LENGTH, TASK_MAX_LENGTH
from aboutlife.overlay import client
from aboutlife.utils import get_resource_path, send_notification, keygrab_loop

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import GObject, Gtk, Gdk, GLib, Vte, Pango

GObject.type_register(Vte.Terminal)

MAX_TERMS = 3
TERM_GAP = 6


class NOTEBOOK(Enum):
    HOME = 0
    SETUP = 1
    BREAK = 2
    TERMINALS = 3


class OverlayPlugin(Plugin):
    def __init__(self):
        self.tick: int = 0
        self.state: STATE = None
        self.end_time: int = int(time.time())
        self.ready: bool = False

        self.main_window = None
        self.focus_window = None

        self.notebook = None
        self.tbx_task = None
        self.cbx_duration = None
        self.swi_network = None
        self.lbl_time = None
        self.lbl_waiting = None
        self.terms = [None] * MAX_TERMS
        self.multiplexer = None

    def setup(self):
        builder = Gtk.Builder()
        builder.add_from_file(get_resource_path("/overlay/ui.glade"))
        builder.connect_signals(self)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(get_resource_path("/overlay/custom.css"))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.main_window = builder.get_object("main-window")
        self.main_window.connect("destroy", Gtk.main_quit)
        self.main_window.connect("delete-event", lambda x, y: True)
        self.main_window.connect("show", self.on_show)
        self.main_window.connect("size-allocate", self.on_resize)
        self.main_window.connect("key-press-event", self.on_key_press)

        self.notebook = builder.get_object("main-notebook")
        self.tbx_task = builder.get_object("tbx-task")
        self.cbx_duration = builder.get_object("cbx-duration")
        self.swi_network = builder.get_object("swi-network")
        self.lbl_time = builder.get_object("lbl-time")
        self.lbl_waiting = builder.get_object("lbl-waiting")
        self.multiplexer = builder.get_object("multiplexer")

        self.tbx_task.set_placeholder_text(f"Mínimo {TASK_MIN_LENGTH} letras")
        self.tbx_task.set_max_length(TASK_MAX_LENGTH)
        self.notebook.set_current_page(NOTEBOOK.SETUP.value)

        # create terminals
        for i in range(MAX_TERMS):
            term_container = builder.get_object(f"term-{i}")
            term = Vte.Terminal()
            term_container.add(term)
            term.connect("button-press-event", self.on_terminal_focus, i)

            # TODO: fallback font
            term.set_font(Pango.FontDescription("IosevkaTermNerdFontMono 12"))
            self.terms[i] = term

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

        # auxiliar regular focusable window to steal focus
        self.focus_window = Gtk.Window()
        self.focus_window.set_title("aboutlife auxiliar window")
        self.focus_window.connect("destroy", Gtk.main_quit)
        self.focus_window.connect("delete-event", lambda x, y: True)
        self.focus_window.set_type_hint(Gtk.WindowType.POPUP)
        self.focus_window.stick()

        # set high priority
        screen = Gdk.Screen.get_default()
        self.main_window.set_default_size(screen.get_width(), screen.get_height())
        self.main_window.fullscreen()
        self.main_window.set_type_hint(Gtk.WindowType.POPUP)
        self.main_window.set_skip_taskbar_hint(True)
        self.main_window.set_skip_pager_hint(True)
        self.main_window.set_keep_above(True)
        self.main_window.set_decorated(False)
        self.main_window.stick()

        # prefer dark theme
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        # start
        self.main_window.show_all()
        self.focus_window.show_all()
        self.ready = True
        Gtk.main()

    def on_show(self, widget):
        # grab keyboard
        thread = threading.Thread(target=keygrab_loop, args=(self.main_window,))
        thread.daemon = True
        thread.start()

        print("D: Starting setting up terminal")
        for i in range(MAX_TERMS):
            term = self.terms[i]
            term.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                os.environ["HOME"],
                ["/usr/bin/env", "bash"],
                ["TMUX="],
                GLib.SpawnFlags.DEFAULT,
            )
        print("D: Done setting up terminal")

    def on_resize(self, a, b):
        print("D: resize event now")
        if MAX_TERMS <= 1:
            return

        overlay_w = self.multiplexer.get_allocated_width()
        overlay_h = self.multiplexer.get_allocated_height()
        gap = TERM_GAP

        # main
        box = self.terms[0].get_parent()
        GLib.idle_add(box.set_margin_top, 0)
        GLib.idle_add(box.set_margin_bottom, 0)
        GLib.idle_add(box.set_margin_start, 0)
        GLib.idle_add(box.set_margin_end, overlay_w / 2 + gap / 2)

        # slaves
        slave_h = overlay_h / (MAX_TERMS - 1)
        for i in range(1, MAX_TERMS):
            print(f"Configuring terminal {i}")
            box = self.terms[i].get_parent()
            margin_top = slave_h * (i - 1) + (gap / 2 if i != 1 else 0)
            margin_bot = slave_h * (MAX_TERMS - 1 - i) + (
                gap / 2 if i != MAX_TERMS - 1 else 0
            )
            GLib.idle_add(box.set_margin_top, margin_top)
            GLib.idle_add(box.set_margin_bottom, margin_bot)
            GLib.idle_add(box.set_margin_start, overlay_w / 2 + gap / 2)
            GLib.idle_add(box.set_margin_end, 0)

    # switch notebook pages (workplaces)
    # TODO: use just pressed
    def on_key_press(self, widget, event) -> bool:
        if not (event.state & Gdk.ModifierType.SUPER_MASK):
            return False

        current = self.notebook.get_current_page()
        if event.keyval == Gdk.KEY_1:
            if self.state == STATE.IDLE:
                if current != NOTEBOOK.HOME.value:
                    GLib.idle_add(self.notebook.set_current_page, NOTEBOOK.HOME.value)
            else:
                if current != NOTEBOOK.BREAK.value:
                    GLib.idle_add(self.notebook.set_current_page, NOTEBOOK.BREAK.value)
            return True
        elif event.keyval == Gdk.KEY_2:
            if current != NOTEBOOK.TERMINALS.value:
                GLib.idle_add(self.notebook.set_current_page, NOTEBOOK.TERMINALS.value)
                self.cycle_terminal_focus(0)
            return True
        elif event.keyval == Gdk.KEY_j:
            self.cycle_terminal_focus(1)
            return True
        elif event.keyval == Gdk.KEY_k:
            self.cycle_terminal_focus(-1)
            return True
        return False

    def on_terminal_focus(self, widget, event, term_i):
        self.cycle_terminal_focus(0, term_i)

    def cycle_terminal_focus(self, step: int, selected_term: int = -1):
        # get which term is focused
        for i in range(MAX_TERMS):
            term = self.terms[i]
            term.get_parent().get_style_context().remove_class("term-selected")

            if selected_term == -1 and term == self.main_window.get_focus():
                selected_term = i

        # select next term or prior
        next_term = (selected_term + step) % MAX_TERMS
        if selected_term == -1:
            next_term = 0

        self.terms[next_term].grab_focus()
        self.terms[next_term].get_parent().get_style_context().add_class(
            "term-selected"
        )

    def process(self):
        self.tick += 1
        if not self.ready:
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
            self.focus_window.present()

            ctx = client.get_state()
            if not ctx:
                print("E: overlay process. couldn't connect to server")
                Gtk.main_quit()
                exit(1)
                return

            prevstate = self.state
            self.state = STATE(ctx.state)
            self.end_time = ctx.end_time

            if self.state == STATE.WORKING:
                print("I: overlay process. state changed to WORKING")
                Gtk.main_quit()
                exit(0)
                return

            text = datetime.now().strftime("%I:%M %p, %d of %B %Y")
            GLib.idle_add(self.lbl_time.set_text, text)

            if prevstate != self.state:
                if (
                    self.state == STATE.TOMATO_BREAK
                    or self.state == STATE.OBLIGATORY_BREAK
                ):
                    GLib.idle_add(self.notebook.set_current_page, NOTEBOOK.BREAK.value)
                else:
                    GLib.idle_add(self.notebook.set_current_page, NOTEBOOK.HOME.value)

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
            network_required = self.swi_network.get_active()

            success = client.put_start_work_session(
                task_info, duration, network_required
            )
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
