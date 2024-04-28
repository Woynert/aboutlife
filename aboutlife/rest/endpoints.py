from enum import Enum


class ENDPOINT(Enum):
    PUT_CLOSE_TABS_RESET = "/close_tabs_reset"
    DELETE_CLOSE_TABS = "/close_tabs"
    GET_STATE = "/state"
    PUT_START_TOMATO_BREAK = "/start_tomato_break"
    PUT_START_WORK_SESSION = "/start_work_session"
    DELETE_SHUTDOWN_SYSTEM = "/shutdown_system"
