import time
import threading
from enum import Enum

TOMATO_BREAK_DURATION = 5 * 60
OBLIGATORY_BREAK_DURATION = 30  # seconds
SHORT_OBLIGATORY_BREAK_DURATION = 8  # seconds
TASK_MAX_LENGHT = 60  # chars
TASK_MAX_DURATION = 50  # minutes


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
        self.duration: int = 0  # minutes
        self.task_info: str = ""
        self.network_required: bool = True
        self.reset()

    def reset(self):
        self.state = STATE.IDLE
        self.close_tabs = False
        self.end_time = 0
        self.duration = 0
        self.task_info = "Sample Task Info"
        self.network_required: bool = True

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

    def setup_work_session(
        self, task_info: str, duration: int, network_required: bool
    ) -> bool:
        if not (
            duration > 0
            and duration <= TASK_MAX_DURATION
            and len(task_info) > 0
            and len(task_info) <= TASK_MAX_LENGHT
            and self.state == STATE.IDLE
        ):
            return False

        self.state = STATE.WORKING
        self.task_info = task_info
        self.network_required = not not network_required
        self.end_time = int(time.time()) + duration * 60
        self.duration = duration
        return True

    def setup_obligatory_break(self) -> bool:
        if self.state != STATE.WORKING:
            return False

        self.state = STATE.OBLIGATORY_BREAK
        self.end_time = int(time.time())

        if self.duration <= 10:
            self.end_time += SHORT_OBLIGATORY_BREAK_DURATION
        else:
            self.end_time += OBLIGATORY_BREAK_DURATION
        return True
