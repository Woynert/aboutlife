import os
import time
import subprocess
import sys
from aboutlife.plugin import Plugin
from aboutlife.context import Context, State


class OverlayWatcherPlugin(Plugin):
    def setup(self):
        interp_path = sys.executable
        script_path = sys.argv[0]
        overlay_active = False

        while True:
            time.sleep(1)
            with Context.get_mutex():
                ctx = Context.get_singleton()
                overlay_active = ctx.state == State.IDLE or ctx.state == State.RESTING

            if overlay_active:
                process = subprocess.Popen(
                    [interp_path, "-m", "aboutlife.overlay.overlay"],
                    cwd=os.path.dirname(script_path) + "/../",
                )
                process.wait()

    def process(self):
        pass

    def health_check(self):
        pass

    def cleanup():
        pass
