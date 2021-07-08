from shared.state_utils import *
from nbt import *

# This will allocate the states to their bricks
def brick_alloc(ir) -> (set, set):
    return NotImplemented


# This will turn a state into a redstone block
def state_to_structure(state: [(WriteInstruction, Direction, int), (WriteInstruction, Direction, int)]) \
        -> nbt.TAG_COMPOUND:
    return NotImplemented


# This will write structure files
def redstonegen(ir) -> (nbt.NBTFile, nbt.NBTFile):
    return NotImplemented
