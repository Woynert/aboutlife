import subprocess
import gi
from Xlib import X, display, protocol

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def send_notification(title: str, message: str):
    if title == "":
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", message])
    else:
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", title, message])


def keygrab_loop(arg_window: Gtk.Window):
    disp = display.Display()
    root = disp.screen().root
    root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)

    while True:
        if disp.pending_events() > 0:
            event = disp.next_event()
            xid = arg_window.get_window().get_xid()
            window = disp.create_resource_object("window", xid)

            if event.type == X.KeyPress:
                event_n = protocol.event.KeyPress(
                    time=0,
                    type=event.type,
                    state=event.state,
                    root=root,
                    window=window,
                    same_screen=0,
                    child=X.NONE,
                    root_x=0,
                    root_y=0,
                    event_x=0,
                    event_y=0,
                    detail=event.detail,
                )
            elif event.type == X.KeyRelease:
                event_n = protocol.event.KeyRelease(
                    time=0,
                    type=event.type,
                    state=event.state,
                    root=root,
                    window=window,
                    same_screen=0,
                    child=X.NONE,
                    root_x=0,
                    root_y=0,
                    event_x=0,
                    event_y=0,
                    detail=event.detail,
                )

            disp.send_event(window, event_n, propagate=False)
            disp.sync()
