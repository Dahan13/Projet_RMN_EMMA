import re
import numpy as np
from datetime import datetime


def data_extractor(path):  # Extracts data from designated file

    """Takes in the JCAMP file's path, then extracts and returns real and imaginary parts as two np.array"""

    with open(path, "r") as f:

        data = []
        # Finds end of Header
        for line in f:
            text = str(line)
            if text == "$$ Real data points\n":
                f.readline()
                f.readline()
                break

        imaginary_index = 0

        for i, line in enumerate(f):
            regex = re.findall(r"\d+[ ]+[-]*\d+", line)
            if regex:
                (x, y) = re.findall(r"[-]*\d+", str(regex[0]))
                if int(x) == 0:  # When finding the second 0 point stocks position of first imaginary
                    imaginary_index = i - 3
                data.append(int(y))
        real_data = np.array(data[:imaginary_index], dtype=int)  # Separates data
        imaginary_data = np.array(data[imaginary_index:], dtype=int)

        f.close()

        # safeguard
        assert len(real_data) == len(imaginary_data), "Data error : different number of real and imaginary parts."
        # end safeguard

        data = np.array([complex(real_data[i], imaginary_data[i]) for i in range(len(real_data))])

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
