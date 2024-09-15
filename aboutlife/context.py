import time
import threading
from enum import Enum

# hour range to be considered 'late'
LATE_HOUR_LOWER = 20
LATE_HOUR_UPPER = 6
# (seconds)
TOMATO_BREAK_DURATION = 5 * 60
OBLIGATORY_BREAK_DURATION = 30
OBLIGATORY_BREAK_DURATION_SHORT = 8
OBLIGATORY_BREAK_DURATION_LATE = 5 * 60
OBLIGATORY_BREAK_THRESHOLD_SHORT = 11 * 60
# (chars)
TASK_MIN_LENGTH = 14
TASK_MAX_LENGTH = 70
TASK_MAX_DURATION = 50  # minutes
TASK_MAX_DURATION_LATE = 25  # minutes


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
        self.reset()

    def reset(self):
        self.state: STATE = STATE.IDLE
        self.close_tabs: bool = False
        self.start_time: int = 0  # unix time from system
        self.end_time: int = 0  # unix time from system
        self.task_info: str = ""
        self.network_required: bool = True
        self.sticky_discrete: bool = False

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
        self,
        task_info: str,
        duration: int,
        network_required: bool,
        sticky_discrete: bool,
    ) -> bool:
        if not (
            duration > 0
            and duration <= TASK_MAX_DURATION
            and (not Context.is_late_hour() or duration <= TASK_MAX_DURATION_LATE)
            and len(task_info) >= TASK_MIN_LENGTH
            and len(task_info) <= TASK_MAX_LENGTH
            and self.state == STATE.IDLE
        ):
            return False

        self.state = STATE.WORKING
        self.task_info = task_info
        self.network_required = not not network_required
        self.sticky_discrete = not not sticky_discrete
        self.start_time = int(time.time())
        self.end_time = int(time.time()) + duration * 60
        return True

    def setup_obligatory_break(self) -> bool:
        if self.state != STATE.WORKING:
            return False

        self.state = STATE.OBLIGATORY_BREAK
        self.end_time = int(time.time())
        elapsed = int(time.time()) - self.start_time  # seconds from task start to now

        if elapsed <= OBLIGATORY_BREAK_THRESHOLD_SHORT:
            self.end_time += OBLIGATORY_BREAK_DURATION_SHORT
        elif Context.is_late_hour():
            self.end_time += OBLIGATORY_BREAK_DURATION_LATE
        else:
            self.end_time += OBLIGATORY_BREAK_DURATION
        return True

    @staticmethod
    def is_late_hour() -> bool:
        curr = time.localtime().tm_hour
        return curr >= LATE_HOUR_LOWER or curr <= LATE_HOUR_UPPER
