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

    spectre = np.fft.ifftshift(spectre_complex)

    signal = np.fft.ifft(spectre)
    signal = np.flip(signal)  # Inversion de tous les termes de la liste

    # Passage de la partie imaginaire à l'opposé pour avoir les mêmes propriétés de sortie que le mode ifft

    signal_real = np.real(signal)
    signal_imaginary = np.imag(signal)

    signal = np.array([complex(signal_real[i], - signal_imaginary[i]) for i in range(n)])

    for i in signal:
        print(i)

else:
    assert 1 == 0, "wrong mode"