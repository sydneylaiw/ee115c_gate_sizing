import numpy as np
from scipy.optimize import minimize
from efforts import *

# Scipy optimize: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

""" Steps:
1. Decide on critical path (on-path)
2. Set optimizer to minimize delay along critical path
3. Set constraints: all delays along branching paths must be equal
4. Output Caps (~W) from optimizer
5. Determine W ratios for NMOS/PMOS (depends on PMOS/NMOS stack lengths)
"""

"""
Current Example (2 branches):
        NAND => INV => Cl = 150
INV =>
        NOR => INV => Cl = 75
"""

""" If we want to truly automate this and not have to manually type in eqns,
    we need to define a tree-like class for path branching,
    which is too much effort
    May reconsider if our paths are super annoying
"""

if __name__ == "__main__":
    # Hard-coded constants
    # Length of full path including multiple branches
    path_len = 4
    # Input cap
    # For all inputs <= 2 unit-invs
    cin = 3
    # Load capacitances (C_par,i + C_gate,i+1)
    # Output of entire circuit loaded with Cl = 32 unit-invs
    Cload1 = 150
    Cload2 = 75

    # Minimization function
    def obj_function(x):
        # Choose critical path (on-path) to minimize
        # d = \sum{fi} + \sum{pi}
        # fi = gi * hi = C_{i+1}/Ci * gi
        # On branches, C_{i+1} = \sum{branch caps}
        return (
            INV.p
            + (x[0] + x[2]) / cin * INV.g
            + +x[1] / x[0] * NAND.g
            + NAND.p
            + Cload1 / x[1] * INV.g
            + INV.p
        )

    # Constraints: delay across all branches must be equal

    # Equal function: returns 0 for constraint met
    def cons1(x):
        # Eqns for branch delay
        # d = \sum{fi} + \sum{pi}
        # fi = gi * hi = C_{i+1}/Ci * gi
        # branch 1
        d1 = x[1] / x[0] * NAND.g + NAND.p + Cload1 / x[1] * INV.g + INV.p
        # branch 2
        d2 = x[3] / x[2] * NOR.g + NOR.p + Cload2 / x[3] * INV.g + INV.p
        return d1 - d2

    # Add more constraint functions/Cloads for more branches
    cons = [{"type": "eq", "fun": cons1}]

    # W cannot be < 1
    bounds = [(1, float("inf")) for i in range(path_len)]

    # set initial values
    # use 1D array for all cap values
    # x0, x1 = NAND, INV (top branch)
    # x2, x3 = NOR, INV (bottom branch)
    x0 = 2 * np.ones(path_len)

    result = minimize(obj_function, x0, constraints=cons, bounds=bounds)
    print(result)
