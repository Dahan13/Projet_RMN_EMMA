import data_handling
import shaped_pulse
from tkinter.filedialog import askopenfilename

filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

module, argument = shaped_pulse.make_number_complex(data_handling.data_extractor(filename))

data_handling.data_writer(module, argument)
