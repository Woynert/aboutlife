import os
import subprocess
import gi
import time
from Xlib import X, display, protocol

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ORIGIN_PATH = os.path.dirname(os.path.realpath(__file__))
GRAB_TIMEOUT = 5
IDLE_TIMEOUT = 0.2


def curr_time() -> int:
    return int(time.time())


def get_resource_path(path: str) -> str:
    return ORIGIN_PATH + path


def send_notification(title: str, message: str):
    if title == "":
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", message])
    else:
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", title, message])


# If there are no keyboard events in a while release it for a moment then grab
# it again, so that the screensaver can take over
def keygrab_loop(arg_window: Gtk.Window):
    disp = display.Display()
    root = disp.screen().root
    xid = arg_window.get_window().get_xid()
    window = disp.create_resource_object("window", xid)
    last_input_time: int = 0
    event_n = None

    while True:
        # try grab it
        grab = root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        if grab != X.GrabSuccess:
            time.sleep(IDLE_TIMEOUT)
            continue

        last_input_time = curr_time()
        while (curr_time() - last_input_time) < GRAB_TIMEOUT:
            if disp.pending_events() > 0:
                # handle events
                last_input_time = curr_time()
                event = disp.next_event()

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
                else:  # skip undesired event
                    continue

                disp.send_event(window, event_n, propagate=False)
                disp.sync()

        # release
        disp.ungrab_keyboard(X.CurrentTime)
        disp.sync()
        time.sleep(IDLE_TIMEOUT)
