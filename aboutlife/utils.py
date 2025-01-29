import os
import subprocess
import gi
import time
import select
from pathlib import Path
from Xlib import X, display, protocol

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ORIGIN_PATH = os.path.dirname(os.path.realpath(__file__))
GRAB_ATTEMPT_TIMEOUT = 1
GRAB_DURATION = 5
IDLE_TIMEOUT = 0.2


## @return seconds
def get_curr_time() -> int:
    return int(time.time())


def get_resource_path(path: str = "") -> str:
    return ORIGIN_PATH + path


def send_notification(title: str, message: str):
    if title == "":
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", message])
    else:
        subprocess.run(["notify-send", "-r", "108", "-t", "1000", title, message])


def get_data_path() -> str:
    xdg_path = Path.home() / ".local" / "share"

    # try to get data path from env
    xdg_path_env: str = os.getenv("XDG_DATA_HOME") or ""
    exists: bool = xdg_path_env != "" and os.path.exists(xdg_path_env)
    if exists:
        xdg_path = Path(xdg_path_env)

    # create if not present
    data_path = xdg_path / "aboutlife"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return str(data_path)


def get_config_path() -> str:
    path = os.path.expanduser("~/.config/aboutlife")
    if not os.path.exists(path):
        os.makedirs(path)
    return str(path)


# * If there are no keyboard events in a while release it for a moment then grab
#   it again, so that the screensaver can take over
# * It's assumed arg_window is ready (use 'show' signal)
def keygrab_loop(arg_window: Gtk.Window):
    disp = display.Display()
    root = disp.screen().root
    fd = disp.fileno()  # display file descriptor
    window = disp.create_resource_object("window", arg_window.get_window().get_xid())
    event_n = None

    while True:
        # try grab keyboard
        grab = root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        if grab != X.GrabSuccess:
            time.sleep(GRAB_ATTEMPT_TIMEOUT)
            continue

        while True:
            # wait for events or timeout
            rlist, _, _ = select.select([fd], [], [], GRAB_DURATION)

            if not rlist:
                # release
                disp.ungrab_keyboard(X.CurrentTime)
                disp.sync()
                time.sleep(IDLE_TIMEOUT)
                break

            while disp.pending_events() > 0:
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
