#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import numpy as np

mode = input("")

if mode == "ifft":

    n = int(input(""))

    real = []
    imaginary = []

    for i in range(n):
        real.append(float(input("")))
    
    for i in range(n):
        imaginary.append(float(input("")))

    signal = np.array([complex(real[i], imaginary[i]) for i in range(len(real))])

    ifft = np.fft.ifft(signal)

    for i in ifft:
        print(i)


else:
    assert 1 == 0, "wrong mode"