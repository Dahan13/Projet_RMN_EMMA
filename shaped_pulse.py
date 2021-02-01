import cmath
import numpy as np


def make_number_complex(data):
    # Prend en argument np.array de réels et np.array d'imaginaires
    # pour retourner np.array de modules et d'arguments (en degrés)

    # safeguard
    if len(data) == 0:
        raise ValueError
    # end safeguard

    # Calcul du module
    module = np.array([abs(data[i]) for i in range(len(data))])
    # Normalisation à 100
    module = [float(i) / max(module) * 100. for i in module]

    # Calcul de l'argument avec modifications pour correspondre aux données du fichier excel
    argument = np.array([-(cmath.phase(i) * 180. / cmath.pi) % 360. for i in data])

    return module, argument
