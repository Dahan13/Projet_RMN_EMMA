import re
import numpy as np

output_file_header = "##TITLE= \n##JCAMP-DX= 5.00 Bruker JCAMP library\n##DATA TYPE= Shape Data\n##ORIGIN= Bruker BioSpin GmbH\n##OWNER= <nmr>\n##DATE= 2012/03/28\n##TIME= 12:31:46\n##$SHAPE_PARAMETERS= Type: Efunc Offset Modulation\n##MINX= 1.000000E-02\n##MAXX= 1.000000E02\n##MINY= 2.250000E00\n##MAXY= 3.577500E02\n##$SHAPE_EXMODE= Excitation\n##$SHAPE_TOTROT= 9.000000E01\n##$SHAPE_TYPE= Excitation\n##$SHAPE_USER_DEF= \n##$SHAPE_REPHFAC= \n##$SHAPE_BWFAC= 1.283480E02\n##$SHAPE_BWFAC50= \n##$SHAPE_INTEGFAC= 6.370927E-03\n##$SHAPE_MODE= 1\n##NPOINTS= 956\n##XYPOINTS= (XY..XY)\n"
output_file_footer = "##END="


def data_extractor(path):  # Extract data from designated file

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
                if int(x) == 0:  # When finding the second 0 point stock position of first imaginary
                    imaginary_index = i - 3
                data.append(int(y))
        real_data = np.array(data[:imaginary_index], dtype=int)  # Separate data
        imaginary_data = np.array(data[imaginary_index:], dtype=int)

        f.close()

        # safeguard
        assert len(real_data) == len(imaginary_data), "Data error : different number of real and imaginary parts."
        # end safeguard

        data = np.array([complex(real_data[i], imaginary_data[i]) for i in range(len(real_data))])

        return data


def data_writer(module, argument, path):

    """Takes in two np.array with modulus and argument and output file's path. Writes data in output file, with hearder and footer."""

    with open(path, "w+") as f:
        # safeguard
        assert len(module) == len(argument), "Data error : different number of modulus and arguments."
        # end safeguard

        f.write(output_file_header)  # Add header
        for i in range(len(module)):  # Write data
            f.write(format(module[i], ".6E") + ", " + format(argument[i], ".6E") + "\n")
        f.write(output_file_footer)  # Add Footer
        f.close()
