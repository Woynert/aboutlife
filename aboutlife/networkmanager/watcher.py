import time
import subprocess
from pathlib import Path
from aboutlife.plugin import Plugin
from aboutlife.context import Context, STATE
from aboutlife.utils import get_resource_path

PATH_INTERNET_BLOCK = "networkmanager/internet_block.sh"
PATH_INTERNET_UNBLOCK = "networkmanager/internet_unblock.sh"


class NetworkManagerPlugin(Plugin):
    def setup(self):
        active = True
        script_internet_block = Path(get_resource_path()) / PATH_INTERNET_BLOCK
        script_internet_unblock = Path(get_resource_path()) / PATH_INTERNET_UNBLOCK

        while True:
            time.sleep(10)

            # it's late + hour is even
            # no_internet_hour = Context.is_late_hour() and (
                # time.localtime().tm_hour % 2 == 0
            # )
            no_internet_hour = Context.is_late_hour()

            if no_internet_hour:
                active = False
            else:
                with Context.get_mutex():
                    ctx = Context.get_singleton()
                    active = ctx.network_required

                    # activate network on any other state
                    if ctx.state != STATE.WORKING:
                        active = True

            # unblock

            command = ["bash", script_internet_unblock]
            process = subprocess.Popen(command)
            process.wait()

            # block

            if not active:
                command = ["bash", script_internet_block]
                process = subprocess.Popen(command)
                process.wait()

            # TODO: detect 'active' change event, and run nmcli down ONCE to make sure all connections are drop

            # if active:
                # command = [
                    # "bash",
                    # "-c",
                    # "( (nmcli n on &) ) &",
                # ]
            # else:
                # command = [
                    # "bash",
                    # "-c",
                    # "( (nmcli n off &) ) &",
                # ]

            # # TODO: Reduce spawn frequency

            # process = subprocess.Popen(command)
            # process.wait()

    def process(self):
        pass

    def cleanup(self):
        pass
