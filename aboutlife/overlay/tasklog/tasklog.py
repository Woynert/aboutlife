from datetime import datetime
import gi
import threading
import time
from typing import List
from aboutlife.overlay.tasklog.fileio import Log, read_log, write_log
from aboutlife.utils import printerr

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
        curr_date = datetime.now()
        self.logs.append(Log(curr_date.hour, curr_date.minute, duration, task))

        # write (blocking)
        write_log(self.logs)

    def _read_logs(self):
        logs = read_log()
        if logs:
            self.logs = logs
            self._logs_fill_missing()
            self._fill_grid()
        else:
            printerr("E: Couldn't load logs")

    def _logs_fill_missing(self):
        filled_logs: List[Log] = []
        curr_hour = datetime.now().hour

        # which hours have log
        hour_has_log: Array[bool] = [False] * 24
        log: Log
        for log in self.logs:
            hour = log.hour % 24
            hour_has_log[hour] = True

        # fill hours that don't have log
        for hour in range(curr_hour + 1):
            if not hour_has_log[hour]:
                filled_logs.append(Log(hour, 0, 0, "---"))
            else:
                log: Log
                for log in self.logs:
                    if log.hour == hour:
                        filled_logs.append(log)

        self.logs = filled_logs

    def _fill_grid(self):
        if not self.grid:
            return

        # Add in reverse order

        j = -1
        for i in range(len(self.logs) - 1, -1, -1):
            j += 1
            log: Log = self.logs[i]
            lbl_hour = Gtk.Label()
            lbl_hour.set_xalign(1)
            lbl_hour.set_yalign(0)

            lbl_task = Gtk.Label()
            lbl_task.set_line_wrap(True)
            lbl_task.set_xalign(0)
            lbl_task.set_yalign(0)

            if log.duration > 0:
                lbl_hour.set_markup(
                    f"{str(log.hour).zfill(2)}:{str(log.minute).zfill(2)}"
                )
                lbl_task.set_markup(f"{log.task} <i>({log.duration}m)</i>")
            else:
                lbl_hour.set_markup(
                    f"<small><i>{str(log.hour).zfill(2)}:{str(log.minute).zfill(2)}</i></small>"
                )
                lbl_task.set_markup("<small>───</small>")

            self.grid.attach(lbl_hour, 0, j, 1, 1)
            self.grid.attach(lbl_task, 1, j, 1, 1)
