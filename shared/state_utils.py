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


def addr_to_full(s, address_to_symbol):
    return f"{address_to_symbol[s]}@{s}"
    # return f"{s}"


def def_to_full(a, address_to_symbol):
    s1 = f"0 -> WRITE {a[0][0]} MOVE {a[0][1]} GOTO {addr_to_full(a[0][2], address_to_symbol)}"
    s2 = f"1 -> WRITE {a[1][0]} MOVE {a[1][1]} GOTO {addr_to_full(a[1][2], address_to_symbol)}"
    return f"[{s1}], [{s2}]"

MAX_ADDRESS = 16383
DIR_TO_INT = {"R": Direction.RIGHT, "L": Direction.LEFT}