import threading
import time
from typing import List
from aboutlife.plugin import Plugin
from aboutlife.tray.tray import TrayPlugin
from aboutlife.overlay.overlay import OverlayPlugin
from aboutlife.rest.rest import RestPlugin
from aboutlife.context import Context

plugins: List[Plugin] = []
plugins_args: List = []
plugins_threads: List[threading.Thread] = []


def process_loop():
    while True:
        print("D: tick")
        for plugin in plugins:
            if not plugin:
                continue
            plugin.process()
        time.sleep(1)


if __name__ == "__main__":
    ctx = Context()
    ctx.reset()

    # setup plugins
    plugins.append(TrayPlugin())
    plugins_args.append([])

    plugins.append(OverlayPlugin())
    plugins_args.append([ctx])

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

    # for thread in plugins_threads:
    # thread.join()

    rest_plugin = RestPlugin()
    rest_plugin.setup(ctx, 8080)
