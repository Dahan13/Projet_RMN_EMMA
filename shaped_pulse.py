# Created by Humbert de Chastellux the 31/01/2021
import math
import numpy as np
import data_handling as dh

path_file = r".\FILE_1_emma21_10010_FID_ANALOG.txt"
real, imaginary = dh.data_extractor(path_file)


def make_number_complex(part_real, part_img):
    # Prend en argument np.array de réels et np.array d'imaginaires
    # pour retourner np.array de modules et d'arguments (en degré)

    # safeguard
    if len(part_real) != 0 and len(part_img) != 0:
        raise ValueError
    # end safeguard

    # Calcul du module
    module = np.array([math.sqrt(part_real[i] ** 2 + part_img[i] ** 2) for i in range(len(part_real))])
    max_module = np.max(module)
    module_norm = np.array([(module[i] / max_module) * 100 for i in range(len(part_real))])

    # Calcul de l'argument
    argument = np.array([ (360 - ((np.arctan( abs(part_img[i] / part_real[i])) / math.pi) * 180)) for i in range(len(part_real))])

    return module_norm, argument


test_value = make_number_complex(real, imaginary)
print(test_value)
