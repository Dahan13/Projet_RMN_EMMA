try:
    import tkinter as tk
except ImportError:
    raise ImportError("\n\nWarning !\nTkinter python library is not installed !\nFor Windows users, your python interpreter version is wrong/broken.\nFor Mac/Linux/Debian users, type \'sudo apt-get install python3-tk\' in a terminal.")
import tkinter.font as font
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os
import sys
import shutil
import configparser
import platform
import re

on_windows = True
try:
    import ctypes.wintypes
except:
    on_windows = False
    if platform.system() == 'Darwin':
        messagebox.showwarning(title="Warning !", message="""
                You are running on MacOS.
                In order for this program to works, python will request aditionnal permissions.
                """)
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')



path_topspin = ""

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
class Wizard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Initializing some fonts for the installer
        self.title_font = font.Font(size = 22, family = 'Calibri')
        self.reg_font = font.Font(size = 11, family = 'Calibri')
        self.button_font = font.Font(size = 11, weight = 'bold')

        self.current_step = None

        # Checking if required modules are installed
        try:
            import numpy
            import scipy
            self.steps = [Step1(self), Step2(self), Step3(self), Step4(self)]
        except ImportError:
            self.steps = [StepImportError(self)]

        # Initializing all widgets
        self.button_frame = tk.Frame(self, bd=1, relief="raised")
        self.content_frame = tk.Frame(self)

        self.back_button = tk.Button(self.button_frame, text="<< Back", command=self.back, font = self.button_font)
        self.next_button = tk.Button(self.button_frame, text="Next >>", command=self.next, font = self.button_font)
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel, font = self.button_font)
        self.finish_button = tk.Button(self.button_frame, text="Finish", command=self.finish, font = self.button_font)

        self.button_frame.pack(side="bottom", fill="x")
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.show_step(0)

    def show_step(self, step):

        if self.current_step is not None:
            # remove current step
            current_step = self.steps[self.current_step]
            current_step.pack_forget()

        self.current_step = step

        new_step = self.steps[step]
        new_step.pack(fill="both", expand=True)

        if len(self.steps) == 1:
            # Special case
            self.back_button.pack_forget()
            self.next_button.pack_forget()
            self.cancel_button.pack_forget()
            self.finish_button.pack(side="right", padx= 20, pady = 5)

        elif step == 0:
            # first step
            self.back_button.pack_forget()
            self.cancel_button.pack(side='right', padx= 20, pady = 5)
            self.next_button.pack(side="right", padx=3, pady=5)
            self.finish_button.pack_forget()

        elif step == len(self.steps)-1:
            # last step
            self.back_button.pack(side="left", padx=3, pady=5)
            self.next_button.pack_forget()
            self.cancel_button.pack_forget()
            self.finish_button.pack(side="right", padx= 20, pady = 5)

        elif step == 2:
            # Step with install button
            self.back_button.pack(side="left", padx=3, pady=5)
            self.cancel_button.pack(side='right', padx= 20, pady = 5)
            self.next_button.pack_forget()
            self.finish_button.pack_forget()

        else:
            # all other steps
            self.back_button.pack(side="left", padx=3, pady=5)
            self.cancel_button.pack(side='right', padx= 20, pady = 5)
            self.next_button.pack(side="right", padx=3, pady=5)
            self.finish_button.pack_forget()
            

    def next(self):
        self.show_step(self.current_step + 1)

    def back(self):
        self.show_step(self.current_step - 1)

    def finish(self):
        self.parent.destroy()

    def cancel(self):
        self.parent.destroy()

class Step1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = tk.Label(self, text="Welcome to the installer setup !", bd=2, relief="groove", font = parent.title_font)
        header.pack(side="top", fill="x")

        content = tk.Label(self, text="""\n
    You are going to install an extension for the TopSpin software from Bruker.
    This installer will guide you through all the steps of the installation.

    This software is provided as is and we will not provide any technical support or be responsible if you damage your machine using this installer.

    Click "Next" to continue.
        """, font = parent.reg_font, justify = "left")
        content.pack()

class Step2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = tk.Label(self, text="TopSpin's main directory", bd=2, relief="groove", font = parent.title_font)
        header.pack(side="top", fill="x")

        content1 = tk.Label(self, text="""
    The installer needs to install a file in the TopSpin software folders.
    Please point to the main TopSpin folder, where topspin.cmd is located.
        """, font = parent.reg_font, justify = "left")
        content1.pack()

        content2 = tk.Frame(self)
        global message
        message = tk.StringVar(content2, value = "Main TopSpin Directory :")
        content3 = tk.Label(content2, textvariable=message)
        content3.pack(side="left", padx=5)
        button = tk.Button(content2, text="Browse...", command=self.browse)
        button.pack(side="right", padx=5)

        content2.pack(pady=20)

    def browse(self):
        """This function will allow the user to browse and select TopSpin main directory"""
        global message
        global path_topspin
        path_topspin = filedialog.askdirectory(title="Specify TopSpin's main folder")
        while (on_windows and not os.path.exists(path_topspin + "/topspin.cmd") or not on_windows and not os.path.exists(path_topspin + "/exp/")) and path_topspin != "":
            messagebox.showwarning(title="Warning !", message="This is not TopSpin's main directory.\nLook for the directory where topspin.cmd is located !")
            path_topspin = filedialog.askdirectory(title="Specify TopSpin's main folder")
        message.set(path_topspin)

class Step3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        header = tk.Label(self, text="Last step", bd=2, relief="groove", font = parent.title_font)
        header.pack(side="top", fill="x")

        content = tk.Label(self, text="""
    Everything is ready for installation
    One file will be installed in the TopSpin folders and two others will be installed in your "Documents" folder.

    Click on "Install" to start the process.
        """, font = parent.reg_font, justify = "left")
        content.pack()

        self.install_button = tk.Button(self, text=" Install ", command = self.install, font = parent.button_font)
        self.install_button.pack(padx=10, pady=10)

        global message2
        message2 = tk.StringVar(self, value = "")
        log = tk.Label(self, textvariable=message2, justify = "left")
        log.pack(pady = 10)

    def install(self):
        global path_topspin
        # Checking if given path to TopSpin directory was correct
        if (on_windows and os.path.exists(path_topspin + "/topspin.cmd") or not on_windows and os.path.exists(path_topspin + "/exp")) and path_topspin != "":
            if on_windows:
                documents_path = get_documents_path()
            else:
                messagebox.showwarning(title="Warning !", message="""
                You are not on Windows.
                Therefore, we will asks you to give us a directory to install the settings.
                This directory must not be protected, we advise you a "Documents" or "Downloads" directory.
                """)
                documents_path = filedialog.askdirectory(title="Settings installation directory")
                if not documents_path or documents_path == "":
                    return
            self.install_button.pack_forget()
            global message2
        

            # Source
            user_directory = r"/exp/stan/nmr/py/user/"
            emma_starter_origin = r"./emma.py"
            deconv_starter_origin = r"./deconv.py"
            deconv_starter_topspin = r"./emma_deconv.py"
            emma_origin = r"./emma_traitement.py"
            deconv_origin = r"./deconv_traitement.py"

            message2.set("Topspin directory set to : \'" + path_topspin + "\'\n")

            if on_windows:
                python_path = (os.path.dirname(sys.executable) + "\python.exe").replace("/", "\\")
            else:
                python_path = (os.path.dirname(sys.executable) + "/python3").replace("\\", "/")
            message2.set(str(message2.get()) + "\nPython path set to : \'" + python_path + "\'\n\n")

            # Create path
            emma_directory = (documents_path + '/EMMA/').replace("\\", "/")
            emma_target = emma_directory + emma_origin[2:]
            deconv_target = emma_directory + deconv_origin[2:]
            emma_starter_target = path_topspin + user_directory + emma_starter_origin[2:]
            deconv_starter_target = path_topspin + user_directory + deconv_starter_topspin[2:]

    
            # Setting up settings file data :
            message2.set(str(message2.get()) + "Building settings file... \n")
            config = configparser.ConfigParser()
            # Getting OS informations
            config.add_section('OS')
            config.set('OS', 'system', str(platform.system()))
            config.set('OS', 'release', str(platform.release()))
            config.set('OS', 'name', str(os.name))

            # Getting path informations
            config.add_section('PATHS')
            config.set('PATHS', 'topspin', str(path_topspin))
            config.set('PATHS', 'python', str(python_path))
            config.set('PATHS', 'emma_directory', str(emma_directory))
            config.set('PATHS', 'emma_starter', str(emma_starter_target))
            config.set('PATHS', 'emma_process', str(emma_target))
            if on_windows:
                config.set('PATHS', 'system32', str(get_system32_location()))

    
            # Preparing emma.py for transfer :
            message2.set(str(message2.get()) + "Writing and copying files to corresponding directories... \n\n")
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

            # Preparing deconv.py for transfer :
            deconv = open(deconv_starter_origin, 'r')
            pattern = re.compile("path_to_settings.*")
            lines = deconv.readlines()
            index = 0
            for line in lines:
                if pattern.match(line):
                    break
                else:
                    index += 1
            lines[index] = f"path_to_settings = \'{emma_directory + 'emma_settings.ini'}\'\n"
            deconv.close()
            # We are making a copy of emma.py that we will copy after updating inside it's path to the settings doc
            new_deconv = open(deconv_starter_origin[:(len(deconv_starter_origin) - 3)] + "_transfert.py", 'w')
            new_deconv.writelines(lines)
            new_deconv.close()

            # Preparing deconv_traitement.py for transfer :
            deconv = open(deconv_origin, 'r')
            pattern = re.compile("path_to_documents.*")
            lines = deconv.readlines()
            index = 0
            for line in lines:
                if pattern.match(line):
                    break
                else:
                    index += 1
            lines[index] = f"path_to_documents = \'{emma_directory}\'\n"
            deconv.close()
            # We are making a copy of emma.py that we will copy after updating inside it's path to the settings doc
            new_deconv = open(deconv_origin[:(len(deconv_origin) - 3)] + "_transfert.py", 'w')
            new_deconv.writelines(lines)
            new_deconv.close()

            # Preparing emma_traitement.py for transfer :
            emma = open(emma_origin, 'r')
            pattern = re.compile("path_to_documents.*")
            lines = emma.readlines()
            index = 0
            for line in lines:
                if pattern.match(line):
                    break
                else:
                    index += 1
            lines[index] = f"path_to_documents = \'{emma_directory}\'\n"
            emma.close()
            # We are making a copy of emma.py that we will copy after updating inside it's path to the settings doc
            new_emma = open(emma_origin[:(len(emma_origin) - 3)] + "_transfert.py", 'w')
            new_emma.writelines(lines)
            new_emma.close()
    
            # Creating directory and moving files
            if not os.path.exists(emma_directory):
                os.mkdir(emma_directory)

            if not os.path.exists(emma_directory + "log/"):
                os.mkdir(emma_directory + "log/")
                message2.set(str(message2.get()) + "EMMA directory created at : \'" + emma_directory + "\'\n")
            shutil.copy(emma_origin, emma_target)

            shutil.copy(deconv_origin[:(len(deconv_origin) - 3)] + "_transfert.py", deconv_target)
            message2.set(str(message2.get()) + "EMMA & Deconv processes successfully moved to : \'" + emma_directory + "\'\n")
            shutil.copy(emma_starter_origin[:(len(emma_starter_origin) - 3)] + "_transfert.py", emma_starter_target)
            message2.set(str(message2.get()) + "EMMA successfully moved to : \'" + emma_starter_target + "\'\n")
            shutil.copy(deconv_starter_origin[:(len(deconv_starter_origin) - 3)] + "_transfert.py", deconv_starter_target)
            message2.set(str(message2.get()) + "DECONV successfully moved to : \'" + deconv_starter_target + "\'\n")
            
            f = open(f"{emma_directory}emma_settings.ini", "w")
            config.write(f)
            f.close()
            message2.set(str(message2.get()) + "Settings file successfully wrote to : \'" + f"{emma_directory}emma_settings.ini\'\n")
            
            # Making widget to go to next page
            end_button = tk.Button(self, text="Next >>", command=self.parent.next, font = self.parent.button_font)
            end_button.pack()
        else:
            message2.set("An invalid path has been provided for the TopSpin main directory")
        

class Step4(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = tk.Label(self, text="Over !", bd=2, relief="groove", font = parent.title_font)
        header.pack(side="top", fill="x")

        content = tk.Label(self, text="""
    The installation is finished!
    Your installation settings have been saved in the "EMMA" folder in your "Documents" folder.

    To change your settings, please restart the installer. Any manual modification will be done at your own risk.

    Instructions on how to use the program are in the file "README.md".
        """, font = parent.reg_font, justify = "left")
        content.pack(pady=5)

class StepImportError(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        header = tk.Label(self, text="Warning !", bd=2, relief="groove", font = parent.title_font)
        header.pack(side="top", fill="x")
        
        content = tk.Label(self, text = '''
    Modules 'numpy' and/or 'scipy' are missing.
    To install them, pip must be installed. To check this, type in the terminal the command : 
> pip --version
    In case you get an error, you must reinstall python by choosing to install pip with it.
    Once pip is installed, to install missing modules, type :
> pip install name_of_the_module
    Be careful, the 'pip' prefix at the beginning of the command may change for some configurations.
        ''', font = parent.reg_font, justify = "left")
        content.pack(pady=5)


window = tk.Tk(className=' Setup interface')
Wizard(window).pack(fill="both", expand=True)
window.resizable(False, False)
window.mainloop()