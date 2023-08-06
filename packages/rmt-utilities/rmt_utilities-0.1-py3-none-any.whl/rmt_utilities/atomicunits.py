"""
some standard units and conversions for use in rmtutil
"""

eV = 0.036749322175655
fs = 41.341374575751
ryd = 0.500000000000
c = 137.036


def au2eV(x):
    """convert atomic units of energy to eV"""
    return x*27.211386245988
