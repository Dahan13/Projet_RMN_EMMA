# Projet_RMN_EMMA

Ce programme nécessite une installation à jour de Python 3.9.x avec les bibliothèque NumPy, TkinTer et SciPy
## Version intégrée :


NE FONCTIONNE QUE SOUS WINDOWS POUR L'INSTANT !

Pour la version intégrée à TopSpin : 

Prend en charge la génération de shape à partir d'un spectre (partie réelle + imaginaire ou réelle seulement).

Installation :
- placer emma_spectrum_to_shape.py dans ...\Topspin4\exp\stan\nmr\py\user
- créer le nouveau dossier ...\Topspin4\exp\stan\nmr\py\emma
- déplacer emma.py dans  ...\Programmes\Topspin4\exp\stan\nmr\py\emma
- actualiser les chemins de fichiers CPYTHON_BIN et CPYTHON_LIB dans emma_spectrum_to_shape.py
- ouvrir le spectre dans TopSpin, lancer la commande edpy et exécuter emma_spectrum_to_shape.py (ou la commande "xpy emma_spectrum_to_shape.py")

## Version manuelle :

Pour la lancer, lancer le fichier main.py situé dans le dossier manual_version. La version manuelle fonctionne normalement sur tous les OS sans problèmes. 

Pour s'en servir, vous n'avez besoin que d'une FID exportée par TopSpin. Nous ne prenons pas en charge des FID exportée par d'autres logiciels.
