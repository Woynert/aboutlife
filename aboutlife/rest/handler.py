import json
from http.server import BaseHTTPRequestHandler
from aboutlife.context import Context


class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path == "/should_close_tabs":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(('{"close":%d}' % True).encode("utf-8"))

        elif self.path == "/state":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            res = ""
            with Context.get_mutex():
                ctx = Context.get_singleton()
                res = json.dumps(
                    {
                        "state": ctx.state.value,
                        "time_end": ctx.time_end,
                    }
                )

            self.wfile.write(res.encode("utf-8"))

    def do_POST(self):
        if self.path == "/start_work_cycle":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)

            self.send_response(200)
            self.end_headers()
