import threading
from enum import Enum


class State(Enum):
    IDLE = 0  # overlay shown
    RESTING = 1  # overlay shown, countdown
    WORKING = 2  # countdown


class Context:
    # static vars
    _mutex = threading.Lock()
    _singleton = None

    def __init__(self):
        self.state: State = State.IDLE
        self.prev_state: State = self.state
        self.time_start: int = 0
        self.time_end: int = 0

    def reset(self):
        self.state = State.IDLE
        self.prev_state: State = self.state
        self.time_start = 0
        self.time_end = 0

    @classmethod
    def get_singleton(cls) -> "Context":
        if cls._singleton == None:
            cls._singleton = cls()
        return cls._singleton

    @classmethod
    def get_mutex(cls) -> threading.Lock:
        return cls._mutex
