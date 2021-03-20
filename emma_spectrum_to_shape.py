#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmath
from subprocess import Popen, PIPE
import re

FILE = 'emma.py'

CPYTHON_BIN = (
        'C:/Windows/System32/cmd.exe /C '
        + 'C:\Users\Lucas\AppData\Local\Programs\Python\Python39\python.exe')
        
CPYTHON_LIB = 'D:/Programmes/Topspin4/exp/stan/nmr/py/emma/'

CPYTHON_FILE = CPYTHON_LIB + FILE
COMMAND_LINE = [CPYTHON_BIN, CPYTHON_FILE]

COMMAND_LINE = " ".join(str(elm) for elm in COMMAND_LINE)


def retrieve_spectrum():
    real = GETPROCDATA(-1000, 1000)
    imaginary = GETPROCDATA(-1000, 1000, type = dataconst.PROCDATA_IMAG)

    if imaginary is not None and imaginary != []: # I don't know what append if there is no imaginary date -> can you test please
        assert len(real) == len(imaginary), "Incorrect data, some real or imaginary numbers are missing"

    return real, imaginary

def ifft((real, imaginary)):

    p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    if imaginary is not None and imaginary != []: # Same here
        SHOW_STATUS('numpy ifft in progress.')
        text = ""
        p.stdin.write("ifft\n")
        p.stdin.write(str(len(real)) + "\n")
        for r in real:
            p.stdin.write(str(r) + "\n")
        for i in imaginary:
            p.stdin.write(str(i) + "\n")

    else:
        SHOW_STATUS('scipy ht and numpy ifft in progress.')
        text = ""
        p.stdin.write("ht\n")
        p.stdin.write(str(len(real)) + "\n")
        for r in real:
            p.stdin.write(str(r) + "\n")

    # Output contains the ifft done in tha emma.py file

    output, err = p.communicate()

    ifft_result = []

    numbers = re.findall(r'.+\d+.+\d+\w.', output)

    for number in numbers:
        if number != []:
            ifft_result.append(complex(number[1:-1]))

    return ifft_result


data = ifft(retrieve_spectrum())

modulus = [abs(data[i]) for i in range(len(data))]
modulus = [float(i) / max(modulus) * 100. for i in modulus]

# phase + modifications

phase = [(cmath.phase(i) * 180. / cmath.pi) % 360. for i in data]

""" text = ""
for i in range(len(modulus)):
    text += str(i) + " : Modulus : " + str(modulus[i]) + " ; Phase : " + str(phase[i])  + "\n"
VIEWTEXT(title="Spectrum to shape", header="Spectrum to shape", text=text)
 """
SAVE_SHAPE("Spectrum to shape", "Spectrum to shape", modulus, phase)

MSG("Shape saved under the name : Spectrum to shape")
