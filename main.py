import data_handling
import shaped_pulse
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

notification_title = "Warning !" # Some memory optimization (and to stop my IDE from bothering me)
save_message = "Save the newly created text document" # Same here
path_error = "Please select a valid path !"

def ask_open_file(title, extension) :

    
    """ Simpler and safer way to ask user to open a file """


    str_title = str(title)
    str_extension = str(extension)
    return filedialog.askopenfilename(title= str_title, defaultextension= str_extension)


def ask_save_file(title, extension) :

    """ Simpler and safer way to ask user to choose path to save file """

    str_title = str(title)
    str_extension = str(extension)
    return filedialog.asksaveasfilename(title= str_title, defaultextension= str_extension)


def write_file(module, argument, output_path):

    """ Handle the final writing of the document """


    # Safeguard if output path is invalid (not a string)
    while output_path == "" or output_path is None:
        messagebox.showwarning(title=notification_title, message= path_error)
        output_path = ask_save_file(save_message, ".txt")

     # Write & save the new document normally
    data_handling.data_writer(module, argument, output_path)


def main_start() :

    """ The main program directing everything. data_handling.py and shaped_pulse.py are mandatory """


    # Asks for the file to use
    filename = ask_open_file("Please select the text document to open.", ".txt")


    # Safeguard, if filename is invalid (not a string)
    while filename == "" or filename is None: 
        messagebox.showwarning(title=notification_title, message= path_error)
        filename = ask_open_file("Please select the text document to open.", ".txt")


    # Handle the calculus and create the new datas
    module, argument = shaped_pulse.make_number_complex(data_handling.data_extractor(filename))


    # Make the user choose path & name for the newly created document
    output_path = ask_save_file(save_message, ".txt")

    # Safeguard if output path is invalid (not a string)
    while output_path == "" or output_path is None:
        messagebox.showwarning(title=notification_title, message= path_error)
        output_path = ask_save_file(save_message, ".txt")


    # Now checking if the user is trying to overwrite datas currently in use
    if output_path == filename :
        alarm = "Output and input path are indentical, initial dataset will be deleted.\nWe rather advise you to create a copy.\nAre you sure about that ?"
        value = messagebox.askyesnocancel(title= notification_title, message= alarm)
        if value is None:
            exit()
        elif value :
            write_file(module, argument, output_path)
        else :
            output_path = ask_save_file(save_message, ".txt")
            write_file(module, argument, output_path)
    # Write & save the new document normally if no occurence between input and output paths
    else :
        write_file(module, argument, output_path)

    
main_start()