#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np
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

else:
    assert 1 == 0, "wrong mode"