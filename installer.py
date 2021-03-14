import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import shutil


def ask_directory(title: str) -> str:
    """ Simpler and safer way to ask user to choose path"""
    str_title = str(title)
    return filedialog.askdirectory(title=str_title)


def ask_open_file(title: str, extension: str = None) -> str:
    """ Simpler and safer way to ask user to give path of a file """
    str_title = str(title)
    str_extension = str(extension)
    return filedialog.askopenfilename(title=str_title, defaultextension=str_extension)


def main():
    # Source
    emma_directory = r"/exp/stan/nmr/py/emma/"
    user_directory = r"/exp/stan/nmr/py/user/"
    emma_starter_origin = r"./emma_spectrum_to_shape.py"
    emma_origin = r"./emma.py"

    # Info from user
    topspin_path = ask_directory("Select Topspin main directory")
    # Safeguard, if directory is invalid (not a string or not topspin)
    while topspin_path == "" or topspin_path is None or not os.path.exists(topspin_path + "/topspin.cmd"):
        messagebox.showwarning(title="Warning !", message="Please select a valid path !")
        topspin_path = ask_directory("Select Topspin main directory")
    print("Topspin directory set to:\n", topspin_path)

    python_path = ask_open_file("Select Python executable")
    # Safeguard, if filename is invalid (not a string)
    while python_path == "" or python_path is None:
        messagebox.showwarning(title="Warning !", message="Please select a valid path !")
        python_path = ask_open_file("Select Python file")
    print("Python path set to:\n", python_path)

    # Create path
    emma_directory = topspin_path + emma_directory
    emma_target = emma_directory + emma_origin[2:]
    emma_starter_target = topspin_path + user_directory + emma_starter_origin[2:]

    # Creating directory and moving files
    if not os.path.exists(emma_directory):
        os.mkdir(emma_directory)
        print("EMMA directory created at:\n", emma_directory)
    shutil.copy(emma_origin, emma_target)
    print("EMMA process successfully moved to: \n", emma_target)
    shutil.copy(emma_starter_origin, emma_starter_target)
    print("EMMA starter successfully moved to: \n", emma_starter_target)

    # Writting settings
    f = open(f"{topspin_path + emma_directory}emma_settings.txt", "w")
    f.write("# OS:\n")
    f.write("Windows\n")
    f.write("# Topspin path: \n")
    f.write(f"{topspin_path}\n")
    f.write("# Python path: \n")
    f.write(f"{python_path}\n")
    f.write("# EMMA directory path: \n")
    f.write(f"{emma_directory}\n")
    f.write("# EMMA starter path: \n")
    f.write(f"{emma_starter_target}\n")
    f.write("# EMMA process path: \n")
    f.write(f"{emma_target}\n")
    f.close()


main()
