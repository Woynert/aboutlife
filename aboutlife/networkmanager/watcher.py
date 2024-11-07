import time
import subprocess
from aboutlife.plugin import Plugin
from aboutlife.context import Context, STATE


class NetworkManagerPlugin(Plugin):
    def setup(self):
        active = True

        while True:
            time.sleep(3)
            with Context.get_mutex():
                ctx = Context.get_singleton()
                active = ctx.network_required

                # activate network on any other state
                if ctx.state != STATE.WORKING:
                    active = True

            command = [
                "bash",
                "-c",
                "( (nmcli n on &) ) &",
            ]

            if not active:
                command = [
                    "bash",
                    "-c",
                    "( (nmcli n off &) ) &",
                ]

            # TODO: Reduce spawn frequency

            process = subprocess.Popen(command)
            process.wait()

    def process(self):
        pass

    def cleanup(self):
        pass
