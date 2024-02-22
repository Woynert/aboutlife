from enum import Enum


class State(Enum):
    CONTROL = 0  # overlay is shown and user is free to start a work session
    WAIT = 1  # waiting an unskipable countdown
    WORK = 2


class Context:
    def __init__(self):
        self.state: State = State.CONTROL
        self.prev_state: State = self.state
        self.time_start: int = 0
        self.time_end: int = 0

    def reset(self):
        self.state = State.CONTROL
        self.prev_state: State = self.state
        self.time_start = 0
        self.time_end = 0
