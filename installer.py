# First, we check that all required modules are installed on the computer :
try:
    import numpy
    import scipy
except ImportError:
    raise ImportError("\n\nWarning !\nPython Modules \'numpy\' and \'scipy\' are mandatory !\n To install each one of them, type \'pip install name_of_the_module\' in the terminal\n")

try:
    import tkinter
except ImportError:
    raise ImportError("\n\nWarning !\nTkinter python library is not installed !\nFor Windows users, your python interpreter version is wrong/broken.\nFor Mac/Linux/Debian users, type \'sudo apt-get install python3-tk\' in a terminal.")
# From now on each module should be installed


import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import sys
import shutil
import ctypes.wintypes
import configparser
import platform
import re


def ask_directory(title: str) -> str:
    """ Simpler and safer way to ask user to choose path"""
    return filedialog.askdirectory(title=str(title))


def ask_open_file(title: str, extension: str = None) -> str:
    """ Simpler and safer way to ask user to give path of a file """
    return filedialog.askopenfilename(title=str(title), defaultextension=str(extension))

def get_documents_path() -> str:
    """This function return the path to Documents windows OS folder"""
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def get_system32_location() -> str:
    """This function give the path to system32 folder"""
    is_wow64 = (platform.architecture()[0] == '32bit' and 'ProgramFiles(x86)' in os.environ)
    system32 = os.path.join(os.environ['SystemRoot'], 'SysNative' if is_wow64 else 'System32')
    return system32.replace("\\", "/")

def main():
    # Source
    user_directory = r"/exp/stan/nmr/py/user/"
    emma_starter_origin = r"./emma.py"
    emma_origin = r"./emma_traitement.py"
    documents_path = get_documents_path()

    # Info from user
    topspin_path = ask_directory("Select Topspin main directory")
    # Safeguard, if directory is invalid (not a string or not topspin)
    while topspin_path == "" or topspin_path is None or not os.path.exists(topspin_path + "/topspin.cmd"):
        messagebox.showwarning(title="Warning !", message="Please select a valid path !")
        topspin_path = ask_directory("Select Topspin main directory")
    print("Topspin directory set to:\n", topspin_path)

    python_path = (os.path.dirname(sys.executable) + "\python.exe").replace("/", "\\")
    print("Python path set to:\n", python_path)

    # Create path
    emma_directory = (documents_path + '/EMMA/').replace("\\", "/")
    emma_target = emma_directory + emma_origin[2:]
    emma_starter_target = topspin_path + user_directory + emma_starter_origin[2:]

    
    # Setting up settings file data :

    config = configparser.ConfigParser()
    # Getting OS informations
    config.add_section('OS')
    config.set('OS', 'system', str(platform.system()))
    config.set('OS', 'release', str(platform.release()))
    config.set('OS', 'name', str(os.name))

    # Getting path informations
    config.add_section('PATHS')
    config.set('PATHS', 'topspin', str(topspin_path))
    config.set('PATHS', 'python', str(python_path))
    config.set('PATHS', 'emma_directory', str(emma_directory))
    config.set('PATHS', 'emma_starter', str(emma_starter_target))
    config.set('PATHS', 'emma_process', str(emma_target))
    config.set('PATHS', 'system32', str(get_system32_location()))

    
    # Preparing emma.py for transfer :
    emma = open(emma_starter_origin, 'r')
    pattern = re.compile("path_to_settings.*")
    lines = emma.readlines()
    index = 0
    for line in lines:
        if pattern.match(line):
            break
        else:
            index += 1
    lines[index] = f"path_to_settings = \'{emma_directory + 'emma_settings.ini'}\'\n"
    emma.close()
    # We are making a copy of emma.py that we will copy after updating inside it's path to the settings doc
    new_emma = open(emma_starter_origin[:(len(emma_starter_origin) - 3)] + "_transfert.py", 'w')
    new_emma.writelines(lines)
    new_emma.close()

    
    # Creating directory and moving files
    if not os.path.exists(emma_directory):
        os.mkdir(emma_directory)
        print("EMMA directory created at:\n", emma_directory)
    shutil.copy(emma_origin, emma_target)
    print("EMMA process successfully moved to: \n", emma_target)
    shutil.copy(emma_starter_origin[:(len(emma_starter_origin) - 3)] + "_transfert.py", emma_starter_target)
    print("EMMA starter successfully moved to: \n", emma_starter_target)
    f = open(f"{emma_directory}emma_settings.ini", "w")
    config.write(f)
    f.close()


    # Finishing
    print(f"\n\n#==============#\nSettings saved at : \'{emma_directory + 'emma_settings.ini'}\'.\nEdit this file at your own risks, to actualize settings, start the installer again.\n#==============#\n")


main()

