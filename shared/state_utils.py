from enum import Enum


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    NONE = None


class WriteInstruction(Enum):
    INVERT = 1
    NOOP = 2


class StateReference():
    symbol = ""
    address = None

    def __init__(self, s, a):
        self.symbol = s
        self.address = a

    def __str__(self):
        return f"{self.symbol}@{self.address}"