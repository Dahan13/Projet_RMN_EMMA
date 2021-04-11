#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np
from scipy.signal import hilbert
import cmath
import math

mode = input("")


if mode == "ifft":

    n = int(input(""))

    real = []
    imaginary = []

    for i in range(n):
        real.append(float(input("")))
    
    for i in range(n):
        imaginary.append(float(input("")))

    n = len(real)

    signal = np.array([complex(real[i], imaginary[i]) for i in range(n)])
    signal = np.fft.ifftshift(signal)

    ifft = np.fft.ifft(signal)

    for i in ifft:
        print(i)

if mode == 'ht':

    n = int(input(""))

    real_spectre = []

    for i in range(n):
        real_spectre.append(float(input("")))

    n = len(real_spectre)

    spectre_complex = hilbert(real_spectre)

    # Passage au complexe conjugué car spectre en entrée
    spectre_complex_real = np.real(spectre_complex)
    spectre_complex_imag = np.imag(spectre_complex)
    spectre_complex = np.array([complex(spectre_complex_real[i], - spectre_complex_imag[i]) for i in range(n)])

    spectre = np.fft.ifftshift(spectre_complex)
    signal = np.fft.ifft(spectre)

    for i in signal:
        print(i)

else:
    assert 1 == 0, "wrong mode"