import sys

peaks_infos = sys.argv[1:][0] # First we take the list containing values
chosen_peak = float(sys.argv[2])
start_log = False

def log(message):
    filename = "C:/Users/Corentin/Documents/EMMA/log_deconv.txt"
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

log("Chosen peak : " + str(chosen_peak))
if peaks_infos != '[]':
    peaks_str = peaks_infos.strip('][').split(', ') # We convert the stringified list into a regular list

    # We convert strings in the list into numbers, all results are in peaks list
    peaks = []
    for element in peaks_str:
        peaks.append(float(element))
else:
    peaks = None
# Peaks is the final list containing peaks other than the one to deconvolve, chosen_peak the one to deconvolve
log("> peaks OK")
n = int(input(""))
log("length : " + str(n))
real = []
imaginary = []

for i in range(n):
    value = float(input(""))
    log("real n°" + str(i) + " : " + str(value))
    real.append(value)

mode = input("")
if mode == "imaginary":
    for i in range(n):
        value = float(input(""))
        log("ima n°" + str(i) + " : " + str(value) )
        imaginary.append(value)


#
#
# Do your things with the data
# 
#

points = [(real[i], imaginary[i]) for i in range(n)]
log(len(str(points)))

counter = 0
for element in points:
    counter += 1
    print(points)


log("> all done")
log("iteration counter :" + str(counter))