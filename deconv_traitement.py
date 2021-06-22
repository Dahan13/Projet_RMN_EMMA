import sys
import time

# Initializing everything
peaks_infos = sys.argv[1:][0] # First we take the list containing values
chosen_peak = float(sys.argv[2])
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


def main():
    log("Chosen peak : " + str(chosen_peak))
    if peaks_infos != '[]':
        peaks_str = peaks_infos.strip('][').split(', ') # We convert the stringified list into a regular list
        # We convert strings in the list into numbers, all results are in peaks list
        peaks = []
        for element in peaks_str:
            peaks.append(float(element.strip("\'")))
    else:
        peaks = None
    # Peaks is the final list containing peaks other than the one to deconvolve, chosen_peak the one to deconvolve
    log("Other peaks : " + str(peaks))

    # Retrieving real and imaginary points
    n = int(input(""))
    real = []
    imaginary = []

    for i in range(n):
        value = float(input(""))
        real.append(value)

    mode = input("")
    if mode == "imaginary":
        for i in range(n):
            value = float(input(""))
            imaginary.append(value)

    log("All spectrum data retrieved !")

    #
    #
    # Do your things with the data
    # 
    #

    points = [(real[i], imaginary[i]) for i in range(n)]

    print(points)
    log("> Points sent successfully")


    log("---> Data treatment Completed <---")

    log("\n\nReal points : " + str(real) + "\n\n")
    log("Imaginary points : " + str(imaginary))

main()