import threading
import time
import urllib.request
from http.server import HTTPServer
from aboutlife.plugin import Plugin
from aboutlife.rest.handler import Handler


DEFAULT_PORT = 13005


class RestPlugin(Plugin):
    def __init__(self):
        self.server = None
        self.port: int = 80

    def setup(self, port: int):
        self.port = port
        self.server = HTTPServer(("127.0.0.1", port), Handler)
        self.server.running = True
        print("D: serving rest")

        while self.server.running:
            self.server.handle_request()

    def process(self):
        pass

    def health_check(self):
        pass

    def cleanup(self):
        self.server.running = False
        # make a request to update the server's running condition
        try:
            urllib.request.urlopen(f"http://localhost:{self.port}")
        except:
            pass
        self.thread.join()


def thread_helper(plugin):
    time.sleep(5)
    # plugin.cleanup()


if __name__ == "__main__":
    plugin = RestPlugin()
    thread = threading.Thread(target=thread_helper, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.setup(DEFAULT_PORT)
