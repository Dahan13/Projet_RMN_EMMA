# Project RMN EMMA

**Table of contents :**
<!-- vscode-markdown-toc -->
* 1. [Program integrated to TopSpin](#VersionintgreTopSpin)
	* 1.1. [Automatic installation of the program](#Installationautomatiqueduprogramme)
		* 1.1.1. [Requirements](#Prrequis)
		* 1.1.2. [Installation](#Installation)
	* 1.2. [Manual installation of the program](#Installationmanuelleduprogramme)
	* 1.3. [How to use](#Utilisationduprogramme)
* 2. [Manual Program](#Versionmanuelle)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
<br>

**Introduction :**

This program requires an up-to-date installation of [Python 3.9.x](https://www.python.org/downloads/) .
During the installation of python, if you are given the choice, also install `pip` and `tkinter`.

Modules `numpy` and `scipy` must also be installed, with :
```bash
> pip install name_of_the_module
```

To install python and pip on Linux/Debian, you may also use :

```bash
> sudo apt install python3 python3-pip
```
Depending of your system, `sudo apt` may need to be replaced by another prefix



##  1. <a name='VersionintgreTopSpin'></a>Program integrated to TopSpin:

This version of the program supports shape generation from a spectrum (real + imaginary part or real only). To use this version you need to have [Bruker's TopSpin software](https://www.bruker.com/protected/en/services/software-downloads/nmr/pc/pc-topspin.html) installed.
###  1.1. <a name='Installationautomatiqueduprogramme'></a>Automatic installation of the program

####  1.1.1. <a name='Prrequis'></a>Requirements

- A system running Windows 8, 8.1 or 10
- A system running under Linux/Debian (Unstable)

####  1.1.2. <a name='Installation'></a>Installation 

Unzip the archive into an unprotected folder on your computer such as the `Downloads` or `Documents` folder. Then open a terminal in the folder where all the files including `installer.py` are located (SHIFT + right click => Open PowerShell for Windows).

Once the terminal is open, type :
```bash
> python3 ./installer.py
```
Be careful, depending on your installation, `python3` may have to be replaced by `py` for it to work.

The program will start the installation, follow these instructions and everything should work fine. 
There is also an alternative installer `installer_shell.py` which does not use a graphical interface but only the terminal.

###  1.2. <a name='Installationmanuelleduprogramme'></a> Manual installation of the program


<br>
This installation is compatible for all platforms, however we provide minimum support for MacOS.
<br>
<br>

- Place `emma.py` in ...\Topspin_folder\exp\stan\nmr\py\user\
- Move `emma_traitement.py` in a folder where you want it, this last one must not be in a secured directory of the machine, to avoid any risk, the  `Documents` folder is the best possible choice.
- Update file paths `CPYTHON_BIN` and `CPYTHON_LIB` in `emma.py`, paying special attention to respect the / (for linux/Debian and MacOS) or \\ (for Windows users).
You can open the file with notepad, some additional instructions are provided in `emma.py` (around line 33, after the `#` character)

###  1.3. <a name='Utilisationduprogramme'></a> How to use
You have to open the spectrum in TopSpin, type the command `edpy` in the bottom left corner and run `emma.py` (or the command "xpy emma.py").

Follow the instructions of the program to save your Shape, then you can use it as you wish

##  2. <a name='Versionmanuelle'></a>Manual Program :

To run it, run `main.py` file located in the `manual_version` folder. The manual version works normally on all OS without problems.

To use it, you only need a FID exported by TopSpin. We do not support FIDs exported by other software.
