import json
from http.server import BaseHTTPRequestHandler
from aboutlife.context import Context
from aboutlife.rest.endpoints import ENDPOINT


class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        if self.path == ENDPOINT.GET_CLOSE_TABS_QUERY.value:
            close_tabs = False
            with Context.get_mutex():
                close_tabs = Context.get_singleton().close_tabs
            self.send_response(200) if close_tabs else self.send_response(403)
            self.end_headers()

        elif self.path == ENDPOINT.GET_STATE.value:
            res = ""
            with Context.get_mutex():
                ctx = Context.get_singleton()
                res = json.dumps(
                    {
                        "state": ctx.state.value,
                        "end_time": ctx.end_time,
                        "task_info": ctx.task_info,
                    }
                )

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(res.encode("utf-8"))

    def do_PUT(self):
        if self.path == ENDPOINT.PUT_CLOSE_TABS_RESET.value:
            with Context.get_mutex():
                Context.get_singleton().close_tabs = False
            self.send_response(200)
            self.end_headers()

        if self.path == ENDPOINT.PUT_START_TOMATO_BREAK.value:
            success = False
            with Context.get_mutex():
                success = Context.get_singleton().setup_tomato_break()

            self.send_response(200) if success else self.send_response(400)
            self.end_headers()

        if self.path == ENDPOINT.PUT_START_WORK_SESSION.value:
            content_length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            task_info = data["task_info"]
            duration = int(data["duration"])

            print(task_info)
            print(duration)

            success = False
            with Context.get_mutex():
                success = Context.get_singleton().setup_work_session(
                    task_info, duration
                )

            self.send_response(200) if success else self.send_response(400)
            self.end_headers()

    def do_DELETE(self):
        if self.path == ENDPOINT.DELETE_CLOSE_TABS.value:
            with Context.get_mutex():
                Context.get_singleton().close_tabs = True
            self.send_response(200)
            self.end_headers()

        if self.path == ENDPOINT.DELETE_SHUTDOWN_SYSTEM.value:
            self.send_response(200)
            self.end_headers()
            print("D: Shutting down")
