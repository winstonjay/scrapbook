'''
vm.py

Simulate a simplified register based runtime enviroment
that takes ARM assembly files as input.

more complexity to be added later.
'''
import sys

def machine(text):
    "Run the simulated ARM code"
    for line in text.splitlines():
        ops = line.strip().replace(",", "").split()
        if len(ops) == 3:
            i1, i2, i3 = ops
            operations[i1](idx(i2), unwraped(i3))
        elif len(ops) == 2:
            i1, i2 = ops
            if i1 != "swi":
                operations[i1](i2)
    return R[0]

def idx(val):
    "return register index number"
    t, d = val[0], int(val[1:])
    return (d if t == "r" else error())

def unwraped(val):
    "return either number literal or register index."
    try: t, d = val[0], int(val[1:])
    except: return val
    return (R[d] if t == "r" else
               d if t == "#" else error())

#### machine operations.

def bl(a):  builtins[a](R[0])
def mov(a, b): R[a] = b
def add(a, b): R[a] += b
def sub(a, b): R[a] -= b
def mul(a, b): R[a] *= b
def error(): raise Exception("invalid value")

operations = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "mov": mov,
    "bl":  bl,
}

# global registers
R = [0 for _ in range(10)]

# builtin simulated functions.
builtins = {
    "ioWrite": print,
    # "ioRead": input,
}

if __name__ == "__main__":
    try: filename = sys.argv[1]
    except:
        raise("Filename required.")
    try:
        with open(filename) as f:
            text = f.read().split("_start:")[1]
        print("simulation exited with status: %d" % machine(text))
    except IOError:
        print("File input error, valid filename required.")