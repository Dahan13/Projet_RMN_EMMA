# Created by Humbert de Chastellux the 31/01/2021
import data_handling as dh
import shaped_pulse as shp

path_file = r".\FILE_1_emma21_10010_FID_ANALOG.txt"
result = shp.make_number_complex(dh.data_extractor(path_file))

print(result)
