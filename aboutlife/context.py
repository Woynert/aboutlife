import time
import threading
from enum import Enum

TOMATO_BREAK_DURATION = 5 * 60
OBLIGATORY_BREAK_DURATION = 30


class STATE(Enum):
    IDLE = 0  # overlay shows
    OBLIGATORY_BREAK = 1  # overlay shows
    TOMATO_BREAK = 2  # overlay shows
    WORKING = 3  # floating message shows


class Context:
    # static vars
    _mutex = threading.Lock()
    _singleton = None

    def __init__(self):
        self.state: STATE = STATE.IDLE
        self.close_tabs: bool = False
        self.end_time: int = 0  # unix time from system
        self.task_info: str = ""
        self.reset()

    def reset(self):
        self.state = STATE.IDLE
        self.close_tabs = False
        self.end_time = 0
        self.task_info = "Sample Task Info"

    @classmethod
    def get_singleton(cls) -> "Context":
        if cls._singleton == None:
            cls._singleton = cls()
        return cls._singleton

    @classmethod
    def get_mutex(cls) -> threading.Lock:
        return cls._mutex

    def setup_tomato_break(self) -> bool:
        if self.state != STATE.IDLE:
            return False

        self.state = STATE.TOMATO_BREAK
        self.end_time = int(time.time()) + TOMATO_BREAK_DURATION
        return True

    def setup_work_session(self, task_info: str, duration: int) -> bool:
        if not (
            duration > 0
            and duration <= 30
            and len(task_info) > 0
            and len(task_info) <= 50
            and self.state == STATE.IDLE
        ):
            return False

        self.state = STATE.WORKING
        self.task_info = task_info
        self.end_time = int(time.time()) + duration * 60
        return True

    def setup_obligatory_break(self) -> bool:
        if self.state != STATE.WORKING:
            return False

        self.state = STATE.OBLIGATORY_BREAK
        self.end_time = int(time.time()) + OBLIGATORY_BREAK_DURATION
        return True
