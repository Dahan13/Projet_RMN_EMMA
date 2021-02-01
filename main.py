# Created by Humbert de Chastellux the 31/01/2021
import data_handling as data_handling
import shaped_pulse as shaped_pulse

path_file = r"datafiles\FILE_1_emma21_10010_FID_ANALOG.txt"

module, argument = shaped_pulse.make_number_complex(data_handling.data_extractor(path_file))

data_handling.data_writer(module, argument)
