import time
from enum import Enum


class State(Enum):
    NONE = 0
    WAIT = 1
    WORK = 2


class Context:
    def __init__(self):
        self.state: State = State.NONE
        self.time_start: int = 0
        self.time_end: int = 0


def context_reset(ctx: Context):
    ctx.state = State.NONE
    ctx.time_start = 0
    ctx.time_end = 0
