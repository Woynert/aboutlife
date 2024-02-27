import time
import subprocess
import sys
from aboutlife.plugin import Plugin
from aboutlife.context import Context, STATE


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
                process = subprocess.Popen([bin_path, "--overlay"])
                process.wait()

    def process(self):
        pass

    def cleanup(self):
        pass
