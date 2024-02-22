from aboutlife.plugin import Plugin
import threading
import time
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/tab_close":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"close":false}')


class RestPlugin(Plugin):
    def __init__(self):
        self.server = None
        self.port = ""

    def setup(self, port):
        self.port = port
        self.server = HTTPServer(("0.0.0.0", port), Handler)
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
    plugin.cleanup()


if __name__ == "__main__":
    plugin = RestPlugin()
    thread = threading.Thread(target=thread_helper, args=(plugin,))
    thread.daemon = True
    thread.start()
    plugin.setup(8080)
