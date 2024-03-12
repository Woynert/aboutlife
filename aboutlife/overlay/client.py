from aboutlife.context import STATE
from aboutlife.rest.endpoints import ENDPOINT
from dataclasses import dataclass
import http.client
import json

HOST = "localhost:8080"


@dataclass
class RespContext:
    state: STATE
    end_time: int
    task_info: str


def get_state() -> RespContext:
    try:
        conn = http.client.HTTPConnection(HOST)
        conn.request("GET", ENDPOINT.GET_STATE.value)
        resp_raw = conn.getresponse()
        conn.close()

        if resp_raw.status == 200:
            resp_json = json.loads(resp_raw.read().decode("utf-8"))
            resp_obj = RespContext(
                resp_json["state"], resp_json["end_time"], resp_json["task_info"]
            )
            return resp_obj
    except Exception as e:
        print(e)
    return None


def delete_close_tabs() -> bool:
    try:
        conn = http.client.HTTPConnection(HOST)
        conn.request("DELETE", ENDPOINT.DELETE_CLOSE_TABS.value)
        resp_raw = conn.getresponse()
        conn.close()

        return resp_raw.status == 200
    except Exception as e:
        print(e)
    return False


def put_start_tomato_break() -> bool:
    try:
        conn = http.client.HTTPConnection(HOST)
        conn.request("PUT", ENDPOINT.PUT_START_TOMATO_BREAK.value)
        resp = conn.getresponse()
        conn.close()

        return resp.status == 200
    except Exception as e:
        print(e)
    return False


def put_start_work_session(
    task_info: str, duration: int, network_required: bool
) -> bool:
    try:
        req_data = json.dumps(
            {
                "task_info": task_info,
                "duration": duration,
                "network_required": network_required,
            }
        )
        headers = {"Content-type": "application/json"}

        conn = http.client.HTTPConnection(HOST)
        conn.request(
            "PUT", ENDPOINT.PUT_START_WORK_SESSION.value, body=req_data, headers=headers
        )
        resp = conn.getresponse()
        conn.close()

        return resp.status == 200
    except Exception as e:
        print(e)
    return False


def delete_shutdown_system() -> bool:
    try:
        conn = http.client.HTTPConnection(HOST)
        conn.request("DELETE", ENDPOINT.DELETE_SHUTDOWN_SYSTEM.value)
        resp_raw = conn.getresponse()
        conn.close()

        return resp_raw.status == 200
    except Exception as e:
        print(e)
    return False
