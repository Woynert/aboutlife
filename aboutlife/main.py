import threading
import time
from typing import Dict, Union, List
from aboutlife.plugin import Plugin
from aboutlife.tray.tray import TrayPlugin
from aboutlife.overlay.overlay import OverlayPlugin
from aboutlife.rest.rest import RestPlugin


# class App:
# def __init__(self):
# # self.ctx = context.Context()
# return

# def set_state(self, state, time=0):
# # self.ctx = context.State.NONE
# return

# def start(self):
# # self.ctx.set_state(context.State.NONE)
# return

# def time_loop(self):
# # TODO: don't loop forever
# return

# def start_loop(self):
# # start steal focus thread
# self.threadTime = threading.Thread(target=self.time_loop)
# self.threadTime.daemon = True
# self.threadTime.start()

plugins: List[Plugin] = []
plugins_args: List = []
plugins_threads: List[threading.Thread] = []


def process_loop():
    while True:
        for plugin in plugins:
            if not plugin:
                continue
            plugin.process()
        time.sleep(1)


if __name__ == "__main__":
    # app = App()
    # app.start()

    # setup plugins
    plugins.append(TrayPlugin())
    plugins_args.append([])

    plugins.append(OverlayPlugin())
    plugins_args.append([])

    plugins.append(RestPlugin())
    plugins_args.append([8080])

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

    while True:
        print("tick")
        # self.time_left -= 1
        # self.label.set_text(str(self.time_left))
        time.sleep(1)
