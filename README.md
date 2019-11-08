
# Simulation de vol groupe 11.13
Ce programme en python permet de simuler et analyser le vol d'une hélice avec  une charge


# Dépendances

Ce programme nécessite d'avoir les trois fichiers dans le meme dossier  
- Propeller.py (fichier qui gère la poussée (lift de l'hélice et la résitance sur l'aile)
- Simulation.py (fichier qui fait tout les calcules de simulations,les graphs et l'analyse)
- main_simulation1113.py(le fichier à démarrer qui s'occupe e "L'UX" et de certaines fonctionnalités de base)
- numpy
- matplotlib


## Fonctionnalités

- Estimation d'un vol à partir d'une vitesse initiale et une charge initiale
- (beta) Recherche d'une vitesse initiale
## Graphiques

Il y'a un graphique par donnée simulée. (vitesse, acc, vitesse radiale,position)
Et aussi un graphique pour la position, la vitesse et l accélération obtenu par une régression polynomiale de la position par la simulation.
Grâce à cette régression, nous constatons que nos simulation sont justes (vu que a = x'') 



