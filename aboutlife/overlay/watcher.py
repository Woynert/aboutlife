import time
import sys
from aboutlife.plugin import Plugin
from aboutlife.context import Context, STATE

PID_PATH = "/tmp/aboutlife_overlay.pid"


class OverlayWatcherPlugin(Plugin):
    def setup(self):
        bin_path = sys.argv[0]
        active = False

        while True:
            time.sleep(1)
            with Context.get_mutex():
                ctx = Context.get_singleton()
                active = ctx.state != STATE.WORKING

            if active:
                self.spawn_if_pid_is_dead(PID_PATH, f"{bin_path} --overlay")

    def process(self):
        pass

    def cleanup(self):
        pass
