#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmath
from posixpath import split
from subprocess import Popen, PIPE
import re

##############################
# Utility functions

# Don't touch the line below, it's meant for the windows installer, touching it with result in breaking the program for every system
path_to_settings = None
###############

def export_settings():

    """ Exports parameters from the settings file """
    if path_to_settings == None:
        MSG("It seems that you didn't launch the installer or the settings are missing, the program will crash.")

    # First we extract all settings from the settings file
    paths = {}
    f = open(path_to_settings, 'r')
    pattern = re.compile("\[.*")
    line = f.readline()
    while len(line):
        if not (pattern.match(line)) and len(line.split(" = ")) == 2:
            paths[line.split(" = ")[0]] = line.split(" = ")[1][:(len(line.split(" = ")[1]) - 1)]
        line = f.readline()
    return paths

def retrieve_spectrum():

    """ Export spectrum data """
    real = GETPROCDATA(-100000, 100000)
    imaginary = GETPROCDATA(-100000, 100000, type = dataconst.PROCDATA_IMAG)

    if imaginary is not None:
        assert len(real) == len(imaginary), "Incorrect data, some real or imaginary numbers are missing"

    return real, imaginary

# End utility functions
#######################

COMMAND_LINE = []
FILE = 'emma_traitement.py'

paths = export_settings()

# Now we will use extracted settings to create the command
if "system32" in paths.keys(): # System32 exists only on windows
    CPYTHON_BIN = (paths['system32'] + '/cmd.exe /C ' + paths['python'])
    CPYTHON_LIB = paths['emma_directory']
else:
    CPYTHON_BIN = paths["python"] 
    CPYTHON_LIB = paths["emma_directory"]

CPYTHON_FILE = CPYTHON_LIB + FILE
COMMAND_LINE = [CPYTHON_BIN, CPYTHON_FILE]
COMMAND_LINE = " ".join(str(elm) for elm in COMMAND_LINE)

def ifft((real, imaginary)):

    if "system32" in paths.keys():
        p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    else:
        p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

    if imaginary is not None:
        SHOW_STATUS('numpy ifft in progress.')
        p.stdin.write("ifft\n")
        p.stdin.write(str(len(real)) + "\n")
        for r in real:
            p.stdin.write(str(r) + "\n")
        for i in imaginary:
            p.stdin.write(str(i) + "\n")

    else:
        SHOW_STATUS('scipy ht and numpy ifft in progress.')
        p.stdin.write("ht\n")
        p.stdin.write(str(len(real)) + "\n")
        for r in real:
            p.stdin.write(str(r) + "\n")

    # Output contains the ifft done in the emma_traitement.py file

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