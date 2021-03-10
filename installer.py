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
    topspin_path = ask_directory("Select Topspin main directory")
    python_path = ask_open_file("Select Python executable")
    # move each file to the right path
    # emma_starter_origin = r".\emma_spectrum_to_shape.py"
    # emma_starter_target = r".\test\emma_spectrum_to_shape.py"
    # shutil.move(emma_starter_origin, emma_starter_target)
    print(python_path, topspin_path)


main()
