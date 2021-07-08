from shared.state_utils import *

MAX_ADDRESS = 16383
DIR_TO_INT = {"R": Direction.RIGHT, "L": Direction.LEFT}


def address(file) -> dict:
    print("Pass 1: Assigning addresses to states.")
    counter = 0
    addresses = dict()
    with open(file, "r") as f:
        for line in f:
            name = line.split("=")[0].replace(" ", "")
            counter += 1
            if counter > max:
                exit(-1)
            addresses[name] = counter
            # print(f"Assigned {counter} to {name}")
        f.close()
    addresses["HALT"] = 0
    print(f"{counter}/{MAX_ADDRESS} addresses used")
    return addresses


def define(address_table, file):
    print("Pass 2: Reading state definitions.")
    states = dict()
    with open(file, "r") as f:
        for line in f:
            val = line.split("=")[1].replace("\n", "").split(" ")[1::]
            # print(val)
            states[address_table[line.split("=")[0].replace(" ", "")]] = [
                (WriteInstruction.NOOP if val[0] == "0" else WriteInstruction.INVERT, DIR_TO_INT[val[1]],
                 address_table[val[2]]),
                (WriteInstruction.NOOP if val[3] == "1" else WriteInstruction.INVERT, DIR_TO_INT[val[4]],
                 address_table[val[5]])]
        states[0] = [(0, None, 0), (0, None, 0)]
        f.close()
    return states


def addr_to_full(s):
    return f"{address_to_symbol[s]}@{s}"
    # return f"{s}"


def def_to_full(a):
    s1 = f"0 -> WRITE {a[0][0]} MOVE {a[0][1]} GOTO {addr_to_full(a[0][2])}"
    s2 = f"1 -> WRITE {a[1][0]} MOVE {a[1][1]} GOTO {addr_to_full(a[1][2])}"
    return f"[{s1}], [{s2}]"


file = "../sample_inputs/zf2.tm"
out = "out.txt"
symbol_to_address_lookup = address(file)
address_to_symbol = {v: k for (k, v) in symbol_to_address_lookup.items()}
address_to_state_def = define(symbol_to_address_lookup, file)

print("ADDR -> DESC")
with open(out, "w") as o:
    o.write(f"states: {len(symbol_to_address_lookup)}\n")
    for (key, value) in address_to_state_def.items():
        o.write(f"{addr_to_full(key)} -> {def_to_full(value)}\n")
    o.flush()
    o.close()
