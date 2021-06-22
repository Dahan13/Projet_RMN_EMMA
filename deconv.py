#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import shutil
from subprocess import Popen, PIPE

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

def peaks_getter():
    list = GETPEAKSARRAY() 
    if not list: 
        MSG("no peaks file found, do 'pp' first") 
        EXIT()
    else:
        peaks_positions = []
        for peak in list:
            peaks_positions.append(str(peak.getIntensity()))
        return peaks_positions

def main((real, imaginary)):
    peaks_positions = peaks_getter()
    # Now generating user interface
    # First, generating a better presentation for peak positions
    peaks_str = ""
    for i in range(len(peaks_positions)):
        peaks_str += str(i + 1) + ": " + str(peaks_positions[i]) + ",\n"
    # Inputing
    result = INPUT_DIALOG("Choose the peak to deconvolve.",
    "Here is peak positions (ppm) given by TopSpin :\n\n" + peaks_str + "\nEnter the position of the peak you want to deconvolve\n(e.g : 1 to deconvolve the first one).",
    ["Position in the list"])[0]
    # Checking that input is a int AND it's a valid value
    while not isinstance(result, int):
        try:
            result = int(result)
            if result < 1 or result > len(peaks_positions):
                result = INPUT_DIALOG("Choose the peak to deconvolve.",
                "Here is peak positions (ppm) given by TopSpin :\n\n" + peaks_str + "\nEnter the position of the peak you want to deconvolve\nPlease make sure you are entering a valid number !",
                ["Position in the list"])[0]
        except ValueError:
            result = INPUT_DIALOG("Choose the peak to deconvolve.",
            "Here is peak positions (ppm) given by TopSpin :\n\n" + peaks_str + "\nEnter the position of the peak you want to deconvolve\nPlease make sure you are entering a valid number !",
            ["Position in the list"])[0]
    chosen_peak = peaks_positions[result - 1]
    del peaks_positions[result - 1]
    
    paths = export_settings()

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
    
    SHOW_STATUS('deconvolve in progress.')
    p.stdin.write(str(len(real)) + "\n")
    for r in real:
        p.stdin.write(str(r) + "\n")
    if imaginary is not None:
        p.stdin.write("imaginary\n")
        for i in imaginary:
            p.stdin.write(str(i) + "\n")
    else:
        p.stdin.write("no\n")

    SHOW_STATUS('deconvolve done. Processing deconvolved data')
    output, err = p.communicate()
    numbers = re.findall(r'.+\d+.+\d+\w.', output)

    return numbers

def save_spectrum(output):

    # Separating real and imaginary list
    real = []
    imaginary = []

    output_str = output.strip('][').replace('(', '').replace(')', '').split(', ') # Separating all our value to compute
    for i in range(0, len(output_str), 2):
        real.append(float(output_str[i]))
        imaginary.append(float(output_str[i+1]))

    # Asking for the name of the new spectrum
    SHOW_STATUS('Saving new spectrum')
    parent_dataset = CURDATA()
    expno = INPUT_DIALOG("Name of the new spectrum",
    "Please choose the name for the deconvolved spectrum.\nThe name must be a number.",
    ["Name of the deconvolved spectrum :"])[0]
    while not isinstance(expno, int):
        try:
            expno = int(expno)
        except ValueError:
            expno = INPUT_DIALOG("Name of the new spectrum",
            "Please choose the name for the deconvolved spectrum.\nTHE NAME MUST BE A NUMBER.",
            ["Name of the deconvolved spectrum :"])[0]
    son_dataset = [parent_dataset[0], str(expno), parent_dataset[2], parent_dataset[3]]

    # Saving the deconvolved spectrum
    path_parent_1 = parent_dataset[3] + '/' + parent_dataset[0] + '/' + parent_dataset[1]
    path_parent_2 = 'pdata/' + parent_dataset[2]
    path_son_1 = parent_dataset[3] + '/' + parent_dataset[0] + '/' + str(expno)
    
    NEWDATASET(son_dataset, path_parent_1, path_parent_2)

    # Warning, despite Topspin parameter copy, there is still missing files that we will handle
    shutil.copy(path_parent_1 + '/acqu', path_son_1 + '/acqu')
    shutil.copy(path_parent_1 + '/acqus', path_son_1 + '/acqus')
    shutil.copy(path_parent_1 + '/' + path_parent_2 + '/procs', path_son_1 + '/' + path_parent_2 + '/procs') # This file was already copied by TopSpin, but it's broken so we redo it

    RE(son_dataset)
    SAVE_ARRAY_AS_1R1I(real, imaginary)
    RE(son_dataset)

    
save_spectrum(main(retrieve_spectrum())[0])