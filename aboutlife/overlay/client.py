from aboutlife.context import State
from dataclasses import dataclass
import http.client
import json

HOST = "localhost:8080"


@dataclass
class StateResponse:
    state: State
    time_left: int


def get_state() -> StateResponse:
    try:
        conn = http.client.HTTPConnection(HOST)
        conn.request("GET", "/state")
        resp_raw = conn.getresponse()
        conn.close()

        if resp_raw.status == 200:
            resp_data = resp_raw.read().decode("utf-8")
            resp_json = json.loads(resp_data)
            resp_obj = StateResponse(resp_json["state"], resp_json["time_left"])
            return resp_obj
    except:
        pass
    return None


def post_start_work_cycle(task_info: str) -> bool:
    try:
        req_data = json.dumps({"task_info": task_info})
        headers = {"Content-type": "application/json"}

        conn = http.client.HTTPConnection(HOST)
        conn.request("POST", "/start_work_cycle", body=req_data, headers=headers)
        resp = conn.getresponse()
        conn.close()

        return resp.status == 200
    except:
        return False
