#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import emma_core as core
from subprocess import Popen, PIPE
import os

def peaks_getter():
    list = GETPEAKSARRAY() 
    if not list: 
        MSG("no peaks file found, do 'pp' first") 
        EXIT()
    else:
        peaks_positions = []
        for peak in list:
            peaks_positions.append(str(peak.getPositions()[0]))
        return peaks_positions

def main():
    peaks_positions = peaks_getter()
    # Now generating user interface
    # First, generating a better presentation for peak positions
    peaks_str = ""
    for i in range(len(peaks_positions)):
        peaks_str += str(i + 1) + ": " + str(peaks_positions[i]) + ",\n"

    # Inputing
    result = int(INPUT_DIALOG("Choose the peak to deconvolve.",
    "Here is peak positions (ppm) given by TopSpin :\n\n" + peaks_str + "\nEnter the position of the peak you want to deconvolve\n(e.g : 1 to deconvolve the first one).",
    ["Position in the list"])[0])
    # Checking user input
    while result < 1 or result > len(peaks_positions) or not result:
        result = int(INPUT_DIALOG("Choose the peak to deconvolve.",
    "Here is peak positions (ppm) given by TopSpin :\n\n" + peaks_str + "\nEnter the position of the peak you want to deconvolve\nPlease make sure you are entering a valid number !",
    ["Position in the list"])[0])
    chosen_peak = peaks_positions[result - 1]
    del peaks_positions[result - 1]

    paths = core.export_settings()

    FILE = "deconv_traitement.py"
    # Now we will use extracted settings to create the command
    if "system32" in paths.keys(): # System32 exists only on windows
        CPYTHON_BIN = paths['python']
        CPYTHON_LIB = paths['emma_directory']
    else:
        CPYTHON_BIN = paths["python"] 
        CPYTHON_LIB = paths["emma_directory"]

    CPYTHON_FILE = CPYTHON_LIB + FILE
    COMMAND_LINE = [CPYTHON_BIN, CPYTHON_FILE, str(peaks_positions), str(chosen_peak)]
    
    COMMAND_LINE = " ".join(str(elm) for elm in COMMAND_LINE)
    
    
    if "system32" in paths.keys():
        p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    else:
        p = Popen(COMMAND_LINE, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

main()