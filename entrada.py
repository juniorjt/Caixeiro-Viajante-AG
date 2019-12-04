# READ INPUT FILE AND CONVERT IT TO REQUIRED FORMAT ----------------------------
def get(filename):
    with open(filename, "r") as f:
        f.readline()
        return ([p.split() for p in f.read().strip().splitlines()])

