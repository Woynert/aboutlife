import threading
import time
from typing import List
from aboutlife.plugin import Plugin
from aboutlife.tray.tray import TrayPlugin
from aboutlife.rest.rest import RestPlugin
from aboutlife.overlay.watcher import OverlayWatcherPlugin
from aboutlife.context import Context, State

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


def main():
    ctx = Context()
    ctx.reset()

    # setup plugins
    plugins.append(TrayPlugin())
    plugins_args.append([])

    plugins.append(RestPlugin())
    plugins_args.append([8080])

    plugins.append(OverlayWatcherPlugin())
    plugins_args.append([])

    for i in range(len(plugins)):
        plugin = plugins[i]
        args = plugins_args[i]

        thread = threading.Thread(target=plugin.setup, args=args)
        thread.daemon = True
        thread.start()
        plugins_threads.append(thread)

    counter = 0

    # process loop
    while True:
        time.sleep(1)
        print("D: tick")

        for plugin in plugins:
            if not plugin:
                continue
            plugin.process()

        counter += 1
        if counter == 5:
            print("UPDATING STATE")
            with Context.get_mutex():
                Context.get_singleton().state = State.WORKING
        if counter == 10:
            print("UPDATING STATE")
            with Context.get_mutex():
                Context.get_singleton().state = State.RESTING
