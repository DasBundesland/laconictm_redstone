from shared.state_utils import *


# START start_read_:
# 	a -> start_write_next; R; a
# 	b -> ERROR; -; b

def address(file) -> dict:
    print("Pass 1: Assigning addresses to states.")
    counter = 0
    addresses = dict()
    with open(file, "r") as f:
        f.readline()
        line = f.readline()
        while line:
            if line == "\n" or line == "":
                line = f.readline()
                continue
            elif line != "":
                counter += 1
                name = line[:-2].replace(" ", "_")
                addresses[name] = counter
                f.readline()
                f.readline()
            line = f.readline()
        f.close()
    addresses["HALT"] = 0
    counter += 1
    addresses["ERROR"] = counter
    print(f"{counter}/{MAX_ADDRESS} addresses used")
    return addresses


def define(address_table, file):
    print("Pass 2: Reading state definitions.")
    states = dict()
    with open(file, "r") as f:
        f.readline()
        line = f.readline()
        addr = None
        while line:
            if line == "" or line == "\n":
                line = f.readline()
                continue
            if line[-2] == ':':
                addr = address_table[line[:-2].replace(" ", "_")]
            if_a = f.readline().replace(" ", "").removesuffix('\n').split("->")[1].split(";")
            if_b = f.readline().replace(" ", "").removesuffix("\n").split("->")[1].split(";")

            t1 = (WriteInstruction.NOOP if if_a[2] == "a" else WriteInstruction.INVERT
                  , DIR_TO_INT[if_a[1]]
                  , address_table[if_a[0]])
            t2 = (WriteInstruction.NOOP if if_b[2] == "b" else WriteInstruction.INVERT
                  , DIR_TO_INT[if_b[1]]
                  , address_table[if_b[0]])
            states[addr] = [t1, t2]
            line = f.readline()
    return states


file = "../sample_inputs/example_tmd_dir.tm2"
out = "out2.txt"
symbol_to_address_lookup = address(file)
# print(symbol_to_address_lookup)
address_to_symbol = {v: k for (k, v) in symbol_to_address_lookup.items()}
address_to_state_def = define(symbol_to_address_lookup, file)

print("ADDR -> DESC")
with open(out, "w") as o:
    o.write(f"states: {len(symbol_to_address_lookup)}\n")
    for (key, value) in address_to_state_def.items():
        o.write(f"{addr_to_full(key, address_to_symbol)} -> {def_to_full(value, address_to_symbol)}\n")
    o.flush()
    o.close()
