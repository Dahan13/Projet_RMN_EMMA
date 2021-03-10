import cmath
import numpy as np


def make_number_complex(data):
    """Takes in two np.array with real and imaginary part and returns two numpy arrays with modulus and adapted argument"""

    # safeguard
    if len(data) == 0:
        raise ValueError
    # end safeguard

    # Modulus
    module = np.array([abs(data[i]) for i in range(len(data))])
    # Normalizing
    module = [float(i) / max(module) * 100. for i in module]

    # Argument + modifications
    argument = np.array([-(cmath.phase(i) * 180. / cmath.pi) % 360. for i in data])

    return module, argument
