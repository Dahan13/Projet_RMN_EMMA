import sys
import os

peaks_infos = sys.argv[1:][0] # First we take the list containing values
chosen_peak = float(sys.argv[2])

if peaks_infos != '[]':
    peaks_str = peaks_infos.strip('][').split(', ') # We convert the stringified list into a regular list

    # We convert strings in the list into numbers, all results are in peaks list
    peaks = []
    for element in peaks_str:
        peaks.append(float(element))
else:
    peaks = None
# Peaks is the final list containing peaks other than the one to deconvolve, chosen_peak the one to deconvolve

# This is to obtain some values to see if the program executed as intended (only use absolute path or TopSpin put the log in an unknown place)
f = open("C:/Users/Corentin/Documents/EMMA/log_deconv.txt", 'w')
f.write(str(peaks) + " " + str(chosen_peak))
f.close()