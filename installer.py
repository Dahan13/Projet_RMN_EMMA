import tkinter.filedialog as filedialog
from typing import Any
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
    emma_directory = r"/test/emma/"
    emma_starter_origin = r"./emma_spectrum_to_shape.py"
    emma_starter_target = r"/test/emma_spectrum_to_shape.py"
    emma_origin = r"./emma.py"
    emma_target = r"emma.py"

    # Info from user
    topspin_path = r"S:\gitstuff\projet_RMN_EMMA"
    python_path = r"S:\anaconda\python.exe"
    # topspin_path = ask_directory("Select Topspin main directory")
    # python_path = ask_open_file("Select Python executable")

    # Create path
    emma_directory = topspin_path+emma_directory
    emma_target = emma_directory+emma_target
    emma_starter_target = topspin_path+emma_starter_target
    print(emma_directory)
    print(emma_target)
    print(emma_starter_target)

    # Creating directory and moving files
    if not os.path.exists(emma_directory):
        os.mkdir(emma_directory)
    shutil.move(emma_origin, emma_target)
    shutil.move(emma_starter_origin, emma_starter_target)


main()
