from utils import *
import collections


# START start_read_:
# 	a -> start_write_next; R; a
# 	b -> ERROR; -; b
class LaconicFrontend:
    @staticmethod
    def address(file) -> dict:
        print("Pass 1: Assigning addresses to states.")
        addr = 0
        addresses = dict()
        with open(file, "r") as f:
            f.readline()
            line = f.readline()
            while line:
                if line == "\n" or line == "":
                    line = f.readline()
                    continue
                elif line != "":
                    addr += 1
                    name = line[:-2].replace(" ", "_")
                    if addr > ERROR_RESERVED or addr == HALT_RESERVED:
                        print(f"Failed to address {name}, there are too many states!")
                        return addresses
                    addresses[name] = addr
                    f.readline()
                    f.readline()
                line = f.readline()
            f.close()
        addresses["HALT"] = HALT_RESERVED
        addresses["ERROR"] = ERROR_RESERVED
        print(f"{len(addresses)}/{(1 << ADDRESS_BITS)} addresses used")
        print(f"Reserved addresses invisible in IR: {0, ERROR_RESERVED}")
        if len(set(addresses.values())) != len(addresses.values()):
            print(f"Address collision is present ({len(set(addresses.values()))}/{len(addresses.values())})")
            print(
                f"Colliding addresses: {[item for item, count in collections.Counter(addresses.values()).items() if count > 1]}")
        # print(addresses)
        return addresses

    @staticmethod
    def define(address_table, file):
        print("Pass 2: Reading state definitions.")
        states = list()
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
                states.append(State(addr, t1, t2))
                line = f.readline()
        states.append(State(HALT_RESERVED, (WriteInstruction.NOOP, None, HALT_RESERVED), (WriteInstruction.NOOP, None, HALT_RESERVED)))
        states.append(State(ERROR_RESERVED, (WriteInstruction.NOOP, None, ERROR_RESERVED), (WriteInstruction.NOOP, None, ERROR_RESERVED)))
        return states

    @staticmethod
    def gen_ir(file, out):
        symbol_to_address_lookup = LaconicFrontend.address(file)
        address_to_state_def = LaconicFrontend.define(symbol_to_address_lookup, file)
        address_to_symbol_lookup = {value: key for (key, value) in symbol_to_address_lookup.items()}
        output_ir_stuff(out,  {a.address: [a.on0, a.on1] for a in address_to_state_def}, address_to_symbol_lookup)
        return address_to_state_def


class NQLFrontend:
    @staticmethod
    def address(file) -> dict:
        print("Pass 1: Assigning addresses to states.")
        addr = 0
        addresses = dict()
        with open(file, "r") as f:
            for line in f:
                name = line.split("=")[0].replace(" ", "")
                addr += 1
                if addr > ERROR_RESERVED or addr == HALT_RESERVED:
                    print(f"Failed to address {name}, there are too many states!")
                addresses[name] = addr
                # print(f"Assigned {counter} to {name}")
            f.close()
        addresses["HALT"] = 0
        print(f"{len(addresses)}/{(1 << ADDRESS_BITS)} addresses used")
        print(f"Reserved addresses invisible in IR: {0, ERROR_RESERVED}")
        if len(set(addresses.values())) != len(addresses.values()):
            print(f"Address collision is present({len(set(addresses.values()))}/{len(addresses.values())})")
            print(
                f"Colliding addresses: {[item for item, count in collections.Counter(addresses.values()).items() if count > 1]}")
        return addresses

    @staticmethod
    def define(address_table, file):
        print("Pass 2: Reading state definitions.")
        states = list()
        with open(file, "r") as f:
            for line in f:
                val = line.split("=")[1].replace("\n", "").split(" ")[1::]
                # print(val)
                curr = State(address_table[line.split("=")[0].replace(" ", "")],
                             (WriteInstruction.NOOP if val[0] == "0" else WriteInstruction.INVERT, DIR_TO_INT[val[1]],
                              address_table[val[2]]),
                             (WriteInstruction.NOOP if val[3] == "1" else WriteInstruction.INVERT, DIR_TO_INT[val[4]],
                              address_table[val[5]]))
                states.append(curr)
            states.append(State(HALT_RESERVED, (WriteInstruction.NOOP, None, HALT_RESERVED), (WriteInstruction.NOOP, None, HALT_RESERVED)))
            f.close()
        return states

    @staticmethod
    def gen_ir(file, out):
        symbol_to_address_lookup = NQLFrontend.address(file)
        address_to_state_def = NQLFrontend.define(symbol_to_address_lookup, file)
        address_to_symbol_lookup = {value: key for (key, value) in symbol_to_address_lookup.items()}
        output_ir_stuff(out, {a.address: [a.on0, a.on1] for a in address_to_state_def}, address_to_symbol_lookup)
        return address_to_state_def


def output_ir_stuff(out, address_to_state_def, address_to_symbol_lookup):
    if out:
        [print(
            f"{addr_to_full(v, address_to_symbol_lookup)} -> {def_to_full(address_to_state_def[v], address_to_symbol_lookup)}")
            for v in address_to_state_def.keys()]
