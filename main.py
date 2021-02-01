import data_handling
import shaped_pulse
import tkinter.filedialog as filedialog

# Asks for the file to use
filename = filedialog.askopenfilename(title="Choisissez le document à ouvrir",
                                      defaultextension=".txt")  # shows an "Open" dialog box and returns the path to the selected file
# Safeguard
if filename == "" or filename is None:
    raise ValueError

# Handle the calculus and create the new document
module, argument = shaped_pulse.make_number_complex(data_handling.data_extractor(filename))

# Make the user choose path & name for the newly created document
output_path = (filedialog.asksaveasfilename(title="Enregistrez le document modifié", defaultextension=".txt"))
# Safeguard
if output_path == "" or output_path is None:
    raise ValueError

# Write & save the new document
data_handling.data_writer(module, argument, output_path)
