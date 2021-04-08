import re
import numpy as np
from datetime import datetime
import math
import tkinter.messagebox as messagebox
import tkinter as tk
import os


def data_extractor(path, from_spectre=False):  # Extracts data from designated file

    """Takes in the JCAMP file's path, then extracts and returns real and imaginary parts as two np.array"""

    with open(path, "r") as f:

        data = []

        for line in f:
            text = str(line)
            # Find total number of point to be filtered
            if re.findall(r"GRPDLY", text):
                grpdly = re.findall(r"GRPDLY=+[ ]+\d.*\d", text)
                grpdly = float(grpdly[0].split("= ")[1])
                filtrable = (grpdly > 0)  # check if the argument has a usable value
                # Round the value of grpdly at the correct value
                print(grpdly)
                grpdly = math.floor(grpdly)
                if grpdly % 2 != 0:
                    grpdly += 1

            # Finds end of Header
            if text == "$$ Real data points\n":
                f.readline()
                f.readline()
                break

        # Find a beacon to determine were is the start of each group
        first_line = re.findall(r"\d+[ ]+[-]*\d+", f.readline())
        (first_x, first_y) = re.findall(r"[-]*\d+", first_line[0])
        beacon = int(first_x)
        data.append(int(first_y))

        for i, line in enumerate(f):
            regex = re.findall(r"\d+[ ]+[-]*\d+", line)
            if regex:
                (x, y) = re.findall(r"[-]*\d+", str(regex[0]))
                if int(x) == beacon:  # When finding the second beacon stocks position of first imaginary
                    imaginary_index = i - 2
                data.append(int(y))
        real_data = np.array(data[:imaginary_index], dtype=int)  # Separates data
        imaginary_data = np.array(data[imaginary_index:], dtype=int)

        f.close()

        # safeguard
        assert len(real_data) == len(imaginary_data), "Data error : different number of real and imaginary parts."
        # end safeguard

        # Filling final dataset with correct values
        data = np.array([complex(real_data[i], imaginary_data[i]) for i in range(len(real_data))])
        # Checking filtering status
        if filtrable:
            # Input for total points (TD) in the inital datas :
            total_points = ask_for_number("Please input the total number of points (real + imaginary) the file have : ", f"{grpdly} points will be edited")

            # Filtering
            data = data_completer(total_points, data, grpdly, from_spectre)
        else:
            messagebox.showwarning(title="Filtering impossible", message="Filtering impossible due to missing \'GRPDLY\' argument")
        return data


def data_writer(module, argument, path):
    """Takes in two np.array with modulus and argument and output file's path. Writes data in output file,
    with hearder and footer. """

    with open(path, "w+") as f:
        # safeguard
        assert len(module) == len(argument), "Data error : different number of modulus and arguments."
        # end safeguard

        f.write(header_creator(module))  # Adds header
        for i in range(len(module)):  # Writes data
            f.write(format(module[i], ".6E") + ", " + format(argument[i], ".6E") + "\n")
        f.write("##END=")  # Adds Footer
        f.close()


def header_creator(table):
    """ Return a proper header with all parameter adapted"""
    number = len(table)
    now = datetime.now()
    date = now.strftime("%Y/%m/%d")
    hour = now.strftime("%H:%M:%S")
    output_file_header = "##TITLE= \n##JCAMP-DX= 5.00 Bruker JCAMP library\n##DATA TYPE= Shape Data\n##ORIGIN= Bruker " \
                         f"BioSpin GmbH\n##OWNER= <nmr>\n##DATE= {date}\n##TIME= {hour}\n##$SHAPE_PARAMETERS= " \
                         "Type: Efunc Offset Modulation\n##MINX= 1.000000E-02\n##MAXX= 1.000000E02\n##MINY= " \
                         "2.250000E00\n##MAXY= 3.577500E02\n##$SHAPE_EXMODE= Excitation\n##$SHAPE_TOTROT= " \
                         "9.000000E01\n##$SHAPE_TYPE= Excitation\n##$SHAPE_USER_DEF= \n##$SHAPE_REPHFAC= " \
                         "\n##$SHAPE_BWFAC= 1.283480E02\n##$SHAPE_BWFAC50= \n##$SHAPE_INTEGFAC= " \
                         f"6.370927E-03\n##$SHAPE_MODE= 1\n##NPOINTS= {number}\n##XYPOINTS= (XY..XY)\n"
    return output_file_header


def data_completer(TD, data, nbr_of_filtered, from_spectre):
    """Execute the filtration depending of if it has already be done"""
    if len(data) * 2 < TD and not from_spectre:  # case if already filtered
        print(f"Completing with {nbr_of_filtered} points...")
        for i in range(nbr_of_filtered):
            data = np.append(data, complex(0, 0))
    elif not from_spectre:  # case if not filtered
        print(f"Filtering {nbr_of_filtered} first points...")
        data = data[nbr_of_filtered:]
        print(f"Completing with {nbr_of_filtered} points...")
        for i in range(nbr_of_filtered):
            data = np.append(data, complex(0, 0))
    elif from_spectre:  # case if FID created from spectre
        print(f"Correcting {nbr_of_filtered} last points...")
        data = data[:nbr_of_filtered]
        print(f"Completing with {nbr_of_filtered} points...")
        for i in range(nbr_of_filtered):
            data = np.append(data, complex(0, 0))
    return data


def ask_for_number(title: str, optionnal_line: str = ""):
    """ Wise use of tkinter to get an int"""

    # Configuration of tkinter window
    master = tk.Tk(className="Number of points to analyse")
    master['bg'] = '#333333'
    tk.Label(
        master,
        text=title + f"\n{optionnal_line}",
        foreground="#EEEEEE",  # Set the text color to white
        background="#333333",  # Set the background color to black
        ).grid(row=0)
    e2 = tk.Entry(master)
    e2.grid(row=2)
    tk.Button(master,
              text='Validate !',
              foreground="#EEEEEE",  # Set the text color to white
              background="#333333",  # Set the background color to black
              command=master.quit).grid(row=3,
                                        column=1,
                                        sticky=tk.W,
                                        pady=4,
                                        padx=4)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    print("Ignore error, it's meant for macOS.")
    master.attributes("-topmost", True)
    master.attributes("-topmost", False)
    master.mainloop()
    # Check if input is an int
    if e2.get().isdigit():
        result = int(e2.get())
        master.destroy()
        return result
    else:
        # Remove the window in use and put a new one
        master.destroy()
        ask_for_number(title, optionnal_line)
