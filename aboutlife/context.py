import time
import threading
from enum import Enum

# hour range to be considered 'late'
LATE_HOUR_LOWER = 20
LATE_HOUR_UPPER = 4

TOMATO_BREAK_SECS = 5 * 60

# when it's considered a "short" session
THRESHOLD_FOR_SHORT_BREAK_SECS = 11 * 60
SHORT_BREAK_SECS = 8
REGULAR_BREAK_SECS = 30

THRESHOLD_LATE_FOR_SHORT_BREAK_SECS = 6 * 60
SHORT_LATE_BREAK_SECS = 8
REGULAR_LATE_BREAK_SECS = 5 * 60

TASK_MIN_LENGTH_CHARS = 0
TASK_MAX_LENGTH_CHARS = 70
TASK_MAX_DURATION_MINS = 50
TASK_MAX_DURATION_LATE_MINS = 10


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
        self.end_time = int(time.time()) + TOMATO_BREAK_SECS
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
            and duration <= TASK_MAX_DURATION_MINS
            and (not Context.is_late_hour() or duration <= TASK_MAX_DURATION_LATE_MINS)
            and len(task_info) >= TASK_MIN_LENGTH_CHARS
            and len(task_info) <= TASK_MAX_LENGTH_CHARS
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

    @staticmethod
    def calculate_break_time_secs(task_duration: int) -> int:
        if not Context.is_late_hour():
            if task_duration < THRESHOLD_FOR_SHORT_BREAK_SECS:
                return SHORT_BREAK_SECS
            else:
                return REGULAR_BREAK_SECS

        # late hour conditions
        else:
            if task_duration < THRESHOLD_LATE_FOR_SHORT_BREAK_SECS:
                return SHORT_LATE_BREAK_SECS
            else:
                return REGULAR_LATE_BREAK_SECS

    def setup_obligatory_break(self) -> bool:
        if self.state != STATE.WORKING:
            return False

        self.state = STATE.OBLIGATORY_BREAK
        curr_time = int(time.time())
        elapsed = curr_time - self.start_time  # seconds from task start to now
        self.end_time = curr_time + Context.calculate_break_time_secs(elapsed)
        return True

    @staticmethod
    def is_late_hour() -> bool:
        curr = time.localtime().tm_hour
        return curr >= LATE_HOUR_LOWER or curr <= LATE_HOUR_UPPER
