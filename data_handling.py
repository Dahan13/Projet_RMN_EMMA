import re
import numpy as np

path_file = r".\FILE_1_emma21_10010_FID_ANALOG.txt"


def data_extractor(path):
    f = open(path, "r")

    data = []

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
            if int(x) == 0:
                imaginary_index = i - 3
            data.append(int(y))

    real_data = np.array(data[:imaginary_index])
    imaginary_data = np.array(data[imaginary_index:])

    return real_data, imaginary_data


def test_data():
    print(data_extractor(path_file))
