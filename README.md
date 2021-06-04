# Projet_RMN_EMMA

**Table des matières :**
<!-- vscode-markdown-toc -->
* 1. [Version intégrée à TopSpin](#VersionintgreTopSpin:)
	* 1.1. [Installation automatique du programme](#Installationautomatiqueduprogramme)
		* 1.1.1. [Prérequis](#Prrequis:)
		* 1.1.2. [Installation](#Installation:)
	* 1.2. [Installation manuelle du programme](#Installationmanuelleduprogramme)
	* 1.3. [Utilisation du programme](#Utilisationduprogramme)
* 2. [Version manuelle](#Versionmanuelle:)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
<br>

**Introduction :**

Ce programme nécessite une installation à jour de [Python 3.9.x](https://www.python.org/downloads/) .
Durant l'installation de python, si on vous laisse le choix, installez également `pip` et `tkinter`.

Les modules `numpy` et `scipy` doivent également être installés, via :
```bash
> pip install name_of_the_module
```



##  1. <a name='VersionintgreTopSpin:'></a>Version intégrée à TopSpin:

Cette version du programme prend en charge la génération de shape à partir d'un spectre (partie réelle + imaginaire ou réelle seulement).
L'utilisation de cette version nécessite d'avoir [le logiciel TopSpin de Bruker](https://www.bruker.com/protected/en/services/software-downloads/nmr/pc/pc-topspin.html) installé.
###  1.1. <a name='Installationautomatiqueduprogramme'></a>Installation automatique du programme

####  1.1.1. <a name='Prrequis:'></a>Prérequis

- Un système sous Windows 8, 8.1 ou 10

####  1.1.2. <a name='Installation:'></a>Installation 

Dézippez l'archive dans un dossier non protégé de votre ordinateur tel que le dossier `Téléchargements` ou `Documents`. Ouvrez ensuite un terminal dans le dossier où se trouvent l'intégralité des fichiers dont `installer.py` (MAJ + clic droit => Ouvrir la fenêtre PowerShell pour Windows).

Une fois le terminal ouvert, tapez :
```bash
> python3 ./installer.py
```
Attention, selon votre installation, `python3` pourra devoir être remplacé par `py` pour que ça marche.

Le programme va démarrer l'installation, suivez ces instructions et tout devrait bien se passer.
Il existe aussi un installeur alternatif `installer_shell.py` qui ne passe pas par une interface graphique mais seulement par le terminal.

###  1.2. <a name='Installationmanuelleduprogramme'></a>Installation manuelle du programme

<br>
Cette installation est compatible pour toutes les plateformes, toutefois nous ne fournissons aucun support pour les machines sous MAC/Linux/Debian.
<br>
<br>

- Placer `emma.py` dans ...\Topspin4\exp\stan\nmr\py\user\
- Déplacez `emma_traitement.py` dans un dossier où vous le souhaiter, ce dernier ne doit pas se trouver dans un répertoire sécurisé de la machine, pour éviter tout risque, le dossier `Documents` est le meilleur choix possible.
- Actualiser les chemins de fichiers `CPYTHON_BIN` et `CPYTHON_LIB` dans `emma.py`, en portant une attention particulière à respecter les / ou \\.
Vous pouvez ouvrir le fichier avec le bloc-note, quelques instructions supplémentaires sont fournis dans `emma.py`

###  1.3. <a name='Utilisationduprogramme'></a>Utilisation du programme
Vous devez ouvrir le spectre dans TopSpin, taper la commande edpy en bas à gauche et exécuter `emma.py` (ou la commande "xpy emma_spectrum_to_shape.py").

Suivez les instructions du programme pour sauvegarder votre Shape, vous pouvez ensuite vous en servir comme vous voulez

##  2. <a name='Versionmanuelle:'></a>Version manuelle :

Pour la lancer, lancez le fichier `main.py` situé dans le dossier `manual_version`. La version manuelle fonctionne normalement sur tous les OS sans problèmes. 

Pour s'en servir, vous n'avez besoin que d'une FID exportée par TopSpin. Nous ne prenons pas en charge des FID exportées par d'autres logiciels.
