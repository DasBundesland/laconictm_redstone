from enum import Enum


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    NONE = None


class WriteInstruction(Enum):
    INVERT = 1
    NOOP = 2


class State:
    address = 0
    on0 = ()
    on1 = ()

    def __init__(self, a, z, o):
        self.address = a
        self.on0 = z
        self.on1 = o


def addr_to_full(s, address_to_symbol):
    return f"{address_to_symbol[s]}@{hex(s)}"
    # return f"{s}"


def def_to_full(a, address_to_symbol):
    s1 = f"0 -> WRITE {a[0][0]} MOVE {a[0][1]} GOTO {addr_to_full(a[0][2], address_to_symbol)}"
    s2 = f"1 -> WRITE {a[1][0]} MOVE {a[1][1]} GOTO {addr_to_full(a[1][2], address_to_symbol)}"
    return f"[{s1}], [{s2}]"


# TODO: Make these configurable by the user

ADDRESS_BITS = 13
ERROR_RESERVED = (1 << ADDRESS_BITS) - 1
HALT_RESERVED = 0
DIR_TO_INT = {"R": Direction.RIGHT, "L": Direction.LEFT, "-": Direction.NONE}
