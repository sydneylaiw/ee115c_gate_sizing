# Logical & Parasitic efforts for logic components
# Update if you add new gates

# Assume:
# - Wp / Wn = 2 / 1
# - Latest-arriving input wired closest to OUT


class INV:
    g = 1
    p = 1


# will we be using multi-input gates?
class NAND:
    # multi-input: g = (N + 2) / 3
    g = 4 / 3
    p = 2


class NOR:
    # multi-input: g = (2N + 1) / 3
    g = 5 / 3
    p = 2


class XOR:
    g = 0
    p = 0


# XOR with transmission gate
class XOR_PTL:
    g = 0
    p = 0
