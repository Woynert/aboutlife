import threading
import time
from typing import List
from aboutlife.plugin import Plugin
from aboutlife.tray.tray import TrayPlugin
from aboutlife.rest.rest import RestPlugin
from aboutlife.overlay.watcher import OverlayWatcherPlugin
from aboutlife.sticky.watcher import StickyWatcherPlugin
from aboutlife.networkmanager.watcher import NetworkManagerPlugin
from aboutlife.context import Context, STATE

plugins: List[Plugin] = []
plugins_args: List = []
plugins_threads: List[threading.Thread] = []


def process_loop():
    while True:
        time.sleep(1)
        print("D: tick")

        with Context.get_mutex():
            ctx = Context.get_singleton()
            if ctx.state != STATE.IDLE and (int(time.time()) > ctx.end_time):
                if ctx.state == STATE.WORKING:
                    ctx.setup_obligatory_break()
                else:
                    ctx.state = STATE.IDLE

        for plugin in plugins:
            if not plugin:
                continue
            plugin.process()


def main():
    Context().get_singleton().reset()

    # setup plugins
    plugins.append(TrayPlugin())
    plugins_args.append([])

    plugins.append(OverlayWatcherPlugin())
    plugins_args.append([])

    plugins.append(StickyWatcherPlugin())
    plugins_args.append([])

    plugins.append(NetworkManagerPlugin())
    plugins_args.append([])

    for i in range(len(plugins)):
        plugin = plugins[i]
        args = plugins_args[i]

        thread = threading.Thread(target=plugin.setup, args=args)
        thread.daemon = True
        thread.start()
        plugins_threads.append(thread)

    # process loop
    thread = threading.Thread(target=process_loop)
    thread.daemon = True
    thread.start()

    rest = RestPlugin()
    rest.setup(8080)
