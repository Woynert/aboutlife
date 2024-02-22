import threading
import time
import urllib.request
from http.server import HTTPServer
from aboutlife.plugin import Plugin
from aboutlife.context import Context
from aboutlife.rest.handler import Handler


class RestPlugin(Plugin):
    def __init__(self):
        self.server = None
        self.port: int = 80
        self.ctx: Context = None

    def setup(self, ctx: Context, port: int):
        self.ctx = ctx
        self.port = port
        self.server = HTTPServer(
            ("0.0.0.0", port),
            lambda *args, **kwargs: Handler(ctx=self.ctx, *args, **kwargs),
        )
        self.server.running = True
        print("D: serving rest")

        while self.server.running:
            print("tick ", self.server.running)
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
    plugin.setup(8080)
