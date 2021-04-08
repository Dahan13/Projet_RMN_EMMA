import data_handling
import shaped_pulse
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter as tk
import os

from_specter = None


def write_file(module, argument, output_path):
    """ Handle the final writing of the document """

    # Write & save the new document normally
    data_handling.data_writer(module, argument, output_path)


def check_filepath(filepath, action: str) -> str:
    """ Check if provided filepath is valid, take an argument to specify which type of path it needs. """

    while not filepath.lower().endswith('.txt') and not (filepath == "" or filepath is None):

        messagebox.showwarning(title="Warning !", message="This is not a text file, please correct it !")
        if action == "open":
            filepath = filedialog.askopenfilename(title="Please select the text document to open.", defaultextension=".txt")
        elif action == "save":
            filepath = filedialog.asksaveasfilename(title="Please select save location", defaultextension=".txt")
    if filepath == "" or filepath is None:
        raise PermissionError("\n### \nUser interrupt \n###\n ")
    return filepath


def two_buttons_choice():
    """ Ask user to choose between to option via graphic mode """
    window = tk.Tk(className="Method option")
    window['bg'] = '#333333'
    global from_specter
    from_specter = False
    label = tk.Label(
        window,
        text="Please choose the right exportation structure :",
        foreground="#EEEEEE",  # Set the text color to white
        background="#333333",  # Set the background color to black
        width=50,
        height=3
    ).pack()

    button1 = tk.Button(
        window,
        text='Normal FID (ANALOG/DIGITAL)',
        foreground="#EEEEEE",
        background="#333333",
        height=1,
        padx=1,
        pady=1,
        command=lambda: window.quit()).pack()

    button2 = tk.Button(
        window,
        text='FID from artificial spectre (i.e was processed by TopSpin)',
        foreground="#EEEEEE",
        background="#333333",
        height=1,
        padx=1,
        pady=1,
        command=lambda: __is_from_specter(window)).pack()
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    print("Ignore error, it's meant for macOS.")
    window.attributes("-topmost", True)
    window.attributes("-topmost", False)
    window.mainloop()


def __is_from_specter(fenetre):
    global from_specter
    from_specter = True
    fenetre.quit()


def ask_open_file(title, extension) -> str:
    """ Simpler and safer way to ask user to open a file """

    return check_filepath(filedialog.askopenfilename(title=str(title), defaultextension=str(extension)), "open")


def ask_save_file(title, extension) -> str:
    """ Simpler and safer way to ask user to choose path to save file """

    return check_filepath(filedialog.asksaveasfilename(title=str(title), defaultextension=str(extension)), "save")


def check_overwrite_status(input_path: str, output_path: str) -> None:
    """ Is gonna handle if the user want to overwrite the input file"""
    while output_path == input_path:
        alarm = "Output and input path are identical, initial dataset will be deleted.\nWe rather advise you to create a copy.\nAre you sure about that ?"
        value = messagebox.askyesnocancel(title="Warning", message=alarm)
        if value is None:
            print("\n\n Process aborted ! \n\n")
            raise SystemExit
        elif value:
            exit()
        else:
            output_path = ask_save_file("Please select new save location", ".txt")


def main_start():
    """ The main program directing everything. data_handling.py and shaped_pulse.py are mandatory """

    # Asks for the file to use
    filename = ask_open_file("Please select the text document to open.", ".txt")

    # Handle the calculus and create the new data
    two_buttons_choice()
    # Dev log
    if from_specter:
        print("Processing from a FID created from a specter EXPERIMENTAL")
    elif not from_specter:
        print("Currently analysing a normal FID (ANALOG/DIGITAL)")
    elif from_specter is None:
        raise ValueError("\n\n WARNING WARNING ! \n#===#\n Wrong value detected for \'from_specter\' variable, please contact the devs")

    datatable = data_handling.data_extractor(filename, from_specter)
    print("Creating Shaped pulse...")
    module, argument = shaped_pulse.make_number_complex(datatable)

    # Make the user choose path & name for the newly created document
    output_path = ask_save_file("Please select where you want to save the output document", ".txt")

    # Now checking if the user is trying to overwrite data currently in use
    check_overwrite_status(filename, output_path)

    # Write & save the new document normally if no occurrences between input and output paths
    write_file(module, argument, output_path)
    print(f"\n#=====#\nFile sucessfully written as \"{output_path}\", no fatal error.\n#=====#\n")


main_start()
