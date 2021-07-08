from shared.state_utils import *


# START start_read_:
# 	a -> start_write_next; R; a
# 	b -> ERROR; -; b
class LaconicFrontend:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def gen_ir(file):
        symbol_to_address_lookup = LaconicFrontend.address(file)
        # print(symbol_to_address_lookup)
        address_to_state_def = LaconicFrontend.define(symbol_to_address_lookup, file)
        return address_to_state_def


class NQLFrontend:
    @staticmethod
    def address(file) -> dict:
        print("Pass 1: Assigning addresses to states.")
        counter = 0
        addresses = dict()
        with open(file, "r") as f:
            for line in f:
                name = line.split("=")[0].replace(" ", "")
                counter += 1
                if counter > MAX_ADDRESS:
                    exit(-1)
                addresses[name] = counter
                # print(f"Assigned {counter} to {name}")
            f.close()
        addresses["HALT"] = 0
        print(f"{counter}/{MAX_ADDRESS} addresses used")
        return addresses

    @staticmethod
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
            states[0] = [(WriteInstruction.NOOP, None, 0), (WriteInstruction.NOOP, None, 0)]
            f.close()
        return states

    @staticmethod
    def gen_ir(file):
        symbol_to_address_lookup = NQLFrontend.address(file)
        address_to_state_def = NQLFrontend.define(symbol_to_address_lookup, file)
        return address_to_state_def
