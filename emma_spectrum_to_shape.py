#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmath
from subprocess import Popen, PIPE

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

	assert len(real) == len(imaginary), "Incorrect data, some real or imaginary numbers are missing"
	
	return real, imaginary

def ifft((real, imaginary)):
	
	p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE)

	SHOW_STATUS('numpy ifft in progress.')
	text = ""
	p.stdin.write("ifft\n")
	p.stdin.write(str(len(real)) + "\n")
	for r in real:
		p.stdin.write(str(r) + "\n")
	for i in imaginary:
		p.stdin.write(str(i) + "\n")
	

	output, err = p.communicate()

	VIEWTEXT(
    title='hello_numpy', header='Output of hello_numpy script',
    text=output+'\n'+err, modal=0)

ifft(retrieve_spectrum())




""" Délivrable 1, là pour stockage


data = [real[i] + 1j * imaginary[i] for i in range(len(real))]

modulus = [abs(data[i]) for i in range(len(data))]
modulus = [float(i) / float(max(modulus)) * 100. for i in modulus]

	# Argument + modifications

phase = [-(cmath.phase(i) * 180. / cmath.pi) % 360. for i in data]
text = "" 
MSG(str(type(phase[0])))




for i in range(len(modulus)):
	text += str(i) + " " + str(phase[i])  + "\n"
VIEWTEXT("GETPROCDATA Test", "Computed modulus", text)

SAVE_SHAPE("test_emma_delivrable_2", "Excitation", phase, modulus)

MSG("Shape saved under the name : ")
"""