# Created by Humbert de Chastellux the 31/01/2021
import math
import numpy as np
import data_handling as dh
path_file = r".\FILE_1_emma21_10010_FID_ANALOG.txt"
real, imaginary = dh.data_extractor(path_file)


def make_number_complex(part_real, part_img):
    # Prend en argument np.array de réels et np.array d'imaginaires
    # pour retourner np.array de modules et d'arguments (en degrés)

    # safeguard
    if len(part_real) == 0 or len(part_img) != len(part_real):
        raise ValueError
    # end safeguard

    # Calcul du module
    module = np.array([math.sqrt(part_real[i] ** 2 + part_img[i] ** 2) for i in range(len(part_real))])
    max_module = np.max(module)
    module_norm = np.array([(module[i] / max_module) * 100 for i in range(len(part_real))])

    # Calcul de l'argument
    argument = np.array([((np.arctan(part_img[i] / part_real[i]) / math.pi) * 180) for i in range(len(part_real))])
    for i in range(len(part_real)):
        if part_real[i] < 0:        # Remise de l'argument sur 360° au lieu de 180°
            argument[i] += 180
        if argument[i] > 0:         # Inversion du sens des angles (trigo -> anti-trigo)
            argument[i] = 360 - argument[i]
        else:
            argument[i] = abs(argument[i])

    return module_norm, argument


module, argument = make_number_complex(real, imaginary)
print(module, argument)

print(module[328])
print(argument[859])