from datetime import datetime
import gi
import threading
import time
from typing import List
from aboutlife.overlay.tasklog.fileio import Log, read_log, write_log

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class TaskLog:
    def __init__(self):
        self.grid: Gtk.Grid = None
        self.logs: List[Log] = []

    # blocking
    def setup(self, builder: Gtk.Builder):
        self.grid = builder.get_object("tasklog-grid")
        self._read_logs()

    def on_start_session(self, task: str, duration: int):
        # append new log
        hour = datetime.now().strftime("%I:%M %p")
        self.logs.append(Log(hour, duration, task))

        # write (blocking)
        write_log(self.logs)

    def _read_logs(self):
        logs = read_log()
        if logs:
            self.logs = logs
            self._fill_grid()

    def _fill_grid(self):
        if not self.grid:
            return

        # Add in reverse order

        j = -1
        for i in range(len(self.logs) - 1, -1, -1):
            j += 1
            log: Log = self.logs[i]
            lbl_hour = Gtk.Label(log.hour)
            lbl_hour.set_xalign(0)
            lbl_hour.set_yalign(0)
            lbl_duration = Gtk.Label(f"({log.duration} mins)")
            lbl_duration.set_xalign(0)
            lbl_duration.set_yalign(0)
            lbl_task = Gtk.Label(log.task)
            lbl_task.set_line_wrap(True)
            lbl_task.set_xalign(0)
            lbl_task.set_yalign(0)

            self.grid.attach(lbl_hour, 0, j, 1, 1)
            self.grid.attach(lbl_duration, 1, j, 1, 1)
            self.grid.attach(lbl_task, 2, j, 1, 1)
