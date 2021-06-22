import sys
import numpy as np
from math import isclose
from math import pi
from copy import copy
import time

start_log = False
path_to_documents = None
actual_time = time.struct_time(time.localtime())

def log(message):
    
    """ This function will dynamically write logs"""
    filename = path_to_documents + "deconv_" + str(actual_time[2]) + "_" + str(actual_time[1]) + "_" + str(actual_time[0]) + "_" + str(actual_time[3]) + "h" + str(actual_time[4]) + "m" + str(actual_time[5]) + "s" + "_log.txt"
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


# Topspin communication functions

def retrieve_spectrum():
    log("Retrieving spectrum from Topspin... ")
    n = int(input(""))
    log("length : " + str(n))
    real = []

    for i in range(n):
        value = float(input(""))
        real.append(value)

    return np.array(real)

def retrieve_peaks():
    log("Retrieving peaks from Topspin...")
    peaks_infos = sys.argv[1:][0] # First we take the list containing values
    chosen_peak = float(sys.argv[2])

    log("Chosen peak : " + str(chosen_peak))

    if peaks_infos != '[]':
        peaks_str = peaks_infos.strip('][').split(', ') # We convert the stringified list into a regular list
        # We convert strings in the list into numbers, all results are in peaks list
        peaks_values = []
        for element in peaks_str:
            peaks_values.append(float(element.strip("\'")))
    else:
        peaks_values = None
    # peaks_values is the final list containing peaks other than the one to deconvolve, chosen_peak the one to deconvolve
    log("Other peaks : " + str(peaks_values))
    log("> Peaks OK !")
    return peaks_values, chosen_peak

def return_spectrum(points):

    log("Returning new spectrum to Topspin... ")

    counter = 0
    for element in points:
        counter += 1
        print(element)

    log("Iteration counter :" + str(counter))
    log("---> Data treatment completed <---")
# Spectrum handling functions

class Peak:
    def __init__(self, x, y, width = 0):
        self.x = x
        self.y = float(y)
        self.width = float(width)
    
    def set_width(self, y_list):

        # Computes peak's width at mid-height

        m = self.y
        i = self.x

        i1 = i
        i2 = i
        width = i
        y_smooth = smooth(y_list)
        while y_smooth[i1 - 1] < y_smooth[i1] or y_smooth[i2 + 1] < y_smooth[i2]:
            if y_smooth[i1 - 1] < y_smooth[i1]:
                i1 -= 1
                if abs(y_list[i1] - m / 2) < abs(y_list[width] - m / 2):
                    width = i1
            if y_smooth[i2 + 1] < y_smooth[i2]:
                i2 += 1
                if abs(y_list[i2] - m / 2) < abs(y_list[width] - m / 2):
                    width = i2
        
        self.width = abs((i - width) * 2)

def find_peak_index(peak, real):
    real_copy = copy(real)
    found = False
    peak = peak * np.max(real) / 10.

    # Makes sure that the nearest value is indeed a peak (otherwise it is set to 0 and we look for the next nearest value)
    
    while not found:
        peak_index = (np.abs(real_copy - peak)).argmin()
        
        if real_copy[peak_index - 1] < real_copy[peak_index] and real_copy[peak_index + 1] < real_copy[peak_index]:
            found = True
        
        else : 
            real_copy[peak_index] = 0
    return peak_index

def smooth(x,window_len=11,window='hanning'):

    # Source : https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html

    if x.ndim != 1:
        raise ValueError

    if x.size < window_len:
        raise ValueError

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]

    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y[int((len(y) - len(x)) / 2): -int((len(y) - len(x)) / 2)]

def derivee(x, y):
    der = [0]
    for i in range(1, len(y) - 1):
        der.append((y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1]))
    der[0] = der[1]
    der.append(der[-1])
    return der

def local_extrema(x_list, y_list, n):

    """returns peaks of given spectrum"""

    smoothed_y = smooth(y_list)
    assert len(smoothed_y) == len(y_list)
    der = derivee(x_list, smoothed_y)

    extrema = []
    for i in range(1, len(smoothed_y)):
        if der[i - 1] * der[i] <= 0:
            j = i
            while(y_list[j + 1] > y_list[j]):
                j += 1
            while(y_list[j - 1] > y_list[j]):
                j += -1
            if [j] not in extrema:
                extrema.append([j])

    for i in range(len(extrema)):
        extrema[i].append(y_list[extrema[i][0]])
    
    extrema.sort(key = lambda x: x[1])
    
    peaks = []

    for extremum in extrema[len(extrema) - n:]:
        peaks.append(Peak(extremum[0], x_list[extremum[0]], extremum[1]))

    for peak in peaks:
        peak.set_width(x_list, y_list)

    return peaks


# Deconvolution functions

def quality(y_list, y):
    
    "lower is better"
    quality_factor = np.sum(abs((y_list - y)))

    return quality_factor

def lorentzian(x_list, x0, gamma, height):
    
    """ Computes lorentzian with given parameters"""

    lorentz = lambda x: gamma / (2 * pi) * 1 / ((gamma ** 2 / 4) + (x - x0) ** 2)
    l = lorentz(x_list)
    m = max(l)
    l = l * (height / m)
    return l

def gaussian(x_list, x0, sigma, height):
    
    """ Computes gaussian with given parameters"""

    gauss = lambda x: 1 / (np.sqrt(pi * 2) * sigma) * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))
    g = gauss(x_list)
    m = max(g)
    g = g * (height / m)
    return g

def mix(x_list, x0, gamma, sigma, height, ratio):

    return ratio * lorentzian(x_list, x0, gamma, height) + (1 - ratio) * gaussian(x_list, x0, sigma, height)

def optimized_mix(x_list, y_list, peak, ratio):

    sigma = peak.width
    gamma = peak.width
    x0 = peak.x
    height = peak.y

    q_ref = quality(y_list, mix(x_list, x0, gamma, sigma, height, ratio))
    q1, q2, q3, q4 = 0, 0, 0, 0
    precision = 0.01
    while not (isclose(q1, q_ref, rel_tol=precision) or isclose(q2, q_ref, rel_tol=precision) or isclose(q3, q_ref, rel_tol=precision) or isclose(q4, q_ref, rel_tol=precision)):
                
        q_ref = min(q1, q2, q3, q4)
        
        if q_ref == q1:
            gamma *= 11./10.
            sigma *= 11./10.
        elif q_ref == q2:
            gamma *= 11./10.
            sigma *= 9./10.
        elif q_ref == q3:
            gamma *= 9./10.
            sigma *= 11./10.
        elif q_ref == q4:
            gamma *= 9./10.
            sigma *= 9./10.

        q1 = quality(y_list, mix(x_list, x0, gamma * 11./10., sigma * 11./10., height, ratio))
        q2 = quality(y_list, mix(x_list, x0, gamma * 11./10., sigma * 9./10., height, ratio))
        q3 = quality(y_list, mix(x_list, x0, gamma * 9./10., sigma * 11./10., height, ratio))
        q4 = quality(y_list, mix(x_list, x0, gamma * 9./10., sigma * 9./10., height, ratio))
        
    return mix(x_list, x0, gamma, sigma, height, ratio)

def deconv(y_list, peaks, peak_index):

    ratio = np.linspace(0, 1, 500)
    x_list = np.array([i for i in range(len(real))])

    best_ratio = ratio[0]
    best_mix = optimized_mix(x_list, y_list, peaks[peak_index], best_ratio)
    best_quality = quality(y_list, best_mix)

    for r in ratio:
        mix = optimized_mix(x_list, y_list, peaks[peak_index], r)
        q = quality(y_list, mix)
        

        if q < best_quality:
            best_quality = q
            best_mix = mix

    return best_mix


real = retrieve_spectrum()
peaks_values, chosen_peak = retrieve_peaks()

peaks_values.append(chosen_peak)
peaks_values.sort()
chosen_index = peaks_values.index(chosen_peak)

peaks = []

for peak_value in peaks_values:
    peaks.append(Peak(find_peak_index(peak_value, real), peak_value))

for peak in peaks:
    peak.set_width(real)

peaks[chosen_index].y = real[peaks[chosen_index].x]

log("> Running deconvolution...")

res = deconv(real, peaks, chosen_index).tolist()

log("> Deconvolution Over !")
    
return_spectrum(res)