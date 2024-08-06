import gi
import threading
from typing import List
from aboutlife.overlay.tasklog.fileio import Log, read_log, write_log

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class TaskLog:
    def __init__(self):
        self.grid: Gtk.Grid = None
        self.logs: List[Log] = []

    def setup(self, builder: Gtk.Builder):
        self.grid = builder.get_object("tasklog-grid")

        # read logs
        thread = threading.Thread(target=self._read_logs)
        thread.daemon = True
        thread.start()

    def update(self):
        self._clear_grid()
        self._fill_grid()

    def _read_logs(self):
        logs = read_log()
        if logs:
            self.logs = logs
        self.update()

    def _clear_grid(self):
        for child in self.grid.get_children():
            GLib.idle_add(self.grid.remove, child)

    def _fill_grid(self):
        for log in self.logs:
            print(log)
            print(log.task)
