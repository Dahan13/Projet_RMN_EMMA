#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.signal import hilbert
import time

start_log = False
path_to_documents = None
actual_time = time.struct_time(time.localtime())

def log(message):
    
    """ This function will dynamically write logs"""

    if path_to_documents != None:
        # Ensuring that log folder exists
        if not os.path.exists(path_to_documents + "log/"):
            os.mkdir(path_to_documents + "log/")
        filename = path_to_documents + "log/" + "emma_" + str(actual_time[2]) + "_" + str(actual_time[1]) + "_" + str(actual_time[0]) + "_" + str(actual_time[3]) + "h" + str(actual_time[4]) + "m" + str(actual_time[5]) + "s" + "_log.txt"
        global start_log
        # This is to obtain some values to see if the program executed as intended (only use absolute path or TopSpin put the log in an unknown place)
        if start_log:
            writing_status = "a"
        else:
            writing_status = "w"
            start_log = True
        f = open(filename, writing_status)
        f.write(str(message) + "\n")
        f.close()

mode = input("")
log("Mode set to : " + str(mode))


if mode == "ifft":

    n = int(input(""))
    log("length : " + str(n))

    real = []
    imaginary = []

    for i in range(n):
        real.append(float(input("")))

    for i in range(n):
        imaginary.append(float(input("")))

    n = len(real)

    log("> Processing data...")
    signal = np.array([complex(real[i], imaginary[i]) for i in range(n)])
    signal = np.fft.ifftshift(signal)

    ifft = np.fft.ifft(signal)

    for i in ifft:
        print(i)

if mode == 'ht':

    n = int(input(""))
    log("length : " + str(n))

    real_spectre = []

    for i in range(n):
        real_spectre.append(float(input("")))

    n = len(real_spectre)

    log("> Processing data...")
    spectre_complex = hilbert(real_spectre)

    # Passage au complexe conjugué car spectre en entrée
    spectre_complex_real = np.real(spectre_complex)
    spectre_complex_imag = np.imag(spectre_complex)
    spectre_complex = np.array([complex(spectre_complex_real[i], - spectre_complex_imag[i]) for i in range(n)])

    spectre = np.fft.ifftshift(spectre_complex)
    signal = np.fft.ifft(spectre)

    log("> Transferring data to TopSpin...")
    for i in signal:
        print(i)
    log("---> Data Treatment complete <---")

else:
    raise ValueError("Wrong mode")
