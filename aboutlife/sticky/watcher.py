import os
import time
import subprocess
import sys
from aboutlife.plugin import Plugin
from aboutlife.context import Context, STATE


class StickyWatcherPlugin(Plugin):
    def setup(self):
        interp_path = sys.executable
        script_path = sys.argv[0]
        active = False

        while True:
            time.sleep(1)
            with Context.get_mutex():
                ctx = Context.get_singleton()
                active = ctx.state == STATE.WORKING

            if active:
                process = subprocess.Popen(
                    [interp_path, "-m", "aboutlife.sticky.sticky"],
                    cwd=os.path.dirname(script_path) + "/../",
                )
                process.wait()

    def process(self):
        pass

    def cleanup(self):
        pass
