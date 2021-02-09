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

    print(real)
    print(imaginary)

else:
    assert 1 == 0, "wrong mode"