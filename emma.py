#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmath
from posixpath import split
from subprocess import Popen, PIPE
import re
import os, sys

COMMAND_LINE = []
FILE = 'emma_traitement.py'
# Don't touch this line, it's meant for the windows installer, touching it with result in breaking the program for every system
path_to_settings = None
###############

if path_to_settings:
    paths = {}
    # First we extract values from settings file and we put all of them in paths as a dictionary
    f = open(path_to_settings, 'r')
    pattern = re.compile("\[.*")
    line = f.readline()
    while len(line):
        if not (pattern.match(line)) and len(line.split(" = ")) == 2:
            paths[line.split(" = ")[0]] = line.split(" = ")[1][:(len(line.split(" = ")[1]) - 1)]
        line = f.readline()
    MSG(str(paths))

    # Now we will use extracted values to create the command
    CPYTHON_BIN = ('C:/Windows/System32/cmd.exe /C ' + paths['python'])
    CPYTHON_LIB = paths['emma_directory']
    CPYTHON_FILE = CPYTHON_LIB + FILE
    COMMAND_LINE = [CPYTHON_BIN, CPYTHON_FILE]

    COMMAND_LINE = " ".join(str(elm) for elm in COMMAND_LINE)
    MSG(COMMAND_LINE)
else:
    # Read each comment after the character '#' to know what to do :
    # Put here the path to python3, it's usually /usr/bin/python3 but here may be some changes depending of your system
    CPYTHON_BIN = ('/path/to/python3')
        
    # Put between the ' characters the path to the folder where emma_traitement.py is located   
    CPYTHON_LIB = '/path/to/EMMA'

    CPYTHON_FILE = CPYTHON_LIB + FILE
    COMMAND_LINE = [CPYTHON_BIN, CPYTHON_FILE]

    COMMAND_LINE = " ".join(str(elm) for elm in COMMAND_LINE)
    MSG(COMMAND_LINE)

def retrieve_spectrum():
    real = GETPROCDATA(-100000, 100000)
    imaginary = GETPROCDATA(-100000, 100000, type = dataconst.PROCDATA_IMAG)

    if imaginary is not None:
        assert len(real) == len(imaginary), "Incorrect data, some real or imaginary numbers are missing"

    return real, imaginary

def ifft((real, imaginary)):

    p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    if imaginary is not None:
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

    # Output contains the ifft done in tha emma_traitement.py file

    output, err = p.communicate()

    ifft_result = []

    numbers = re.findall(r'.+\d+.+\d+\w.', output)

    for number in numbers:
        if number != []:
            ifft_result.append(complex(number[1:-1]))

    return ifft_result


data = ifft(retrieve_spectrum())

# Modulus normalization

modulus = [abs(data[i]) for i in range(len(data))]
modulus = [float(i) / max(modulus) * 100. for i in modulus]

# phase + modifications

phase = [(cmath.phase(i) * 180. / cmath.pi) % 360. for i in data]

shape_name = str(INPUT_DIALOG("EMMA", "Entrez le nom de la shape a enregistrer", ["Name = "], ["Shape"], ["",""], ["1", "1"])[0])
SAVE_SHAPE(str(shape_name), str(shape_name), modulus, phase)
MSG("Shape saved under the name : " + shape_name)
