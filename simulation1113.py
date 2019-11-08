import math
import matplotlib.pyplot as plt
import numpy as np
import propeller
import simulation


#statics
m = 0.027
I = 0.5*0.027*0.0875**2
bladeGeom = np.array([[0.0135, np.pi/9, 0.025], [0.0730, np.pi/9, 0.039]])


vol = simulation.Simulation(bladeGeom,I)

#welcome
print("------------ BIENVENUE AU SIMULATEUR DU GROUPE 11.13 -------------- \n")
print("------------     Donnees de base non modifiable     -------------- \n\n")
print("Duree max du vol autorise (protection anti con pour les intimes): ",vol.end,"s")
print("une inertie de: ",vol.I,"kg.m² elle est balaise hein :p")
print("Avec une gravite de: ",vol.g,"m/s² bravo l'originialite groupe 11.13")
print("Bref après ces messages inutiles, que vous ne lirez pas, veuillez entrer:\n\n ")


#fonctions helpers pour l'interaction avec l utilsiateur
def askCharge():
  try:
    charge = int(input("La charge a transporter (en g) > "))
  except Exception as e:
    charge = 0
  charge = charge/1000.0
  return(charge)

def handleManual():
  """
  Gere le mode manuel => on entre une vitesse et ressort l altitude
  args:
    /
  return:
    graphs, analyse de la simulation, regression de la simulation
  """
  w0 = int(input("Vitesse en tour/seconde de l'helice > "))

  mVol = askCharge() + m
  w0 = w0*2*np.pi
  vol.simulate(w0,mVol)
  vol.simulationGraph()
  vol.analyseSimulation(True)
  vol.SimulationToPolynomial(True)
  plt.show()

def handleSearch():
  """
  Gere la recherche de la vitesse initiale necessaire pour aller a une hauteur X
  (beta)
  args
  /
  returns :
  graphs de la simulation et resultats

  """
  minimum = 30
  maximum = 150
  steps = 5
  trouve = 0
  last = 0
  cherche = 3
  m = 0.027 + askCharge()
  regress = []
  print("Creation de la regression a basse precision pour cette masse")
  s = simulation.Simulation(bladeGeom,I,0.2)
  fastRange = range(minimum,maximum,steps)
  for i in fastRange:
    w = i*2*np.pi
    s.simulate(w,m)
    ymax,tmax = s.analyseSimulation()
    regress.append(ymax)
  fastResearch = np.polyfit(regress,list(fastRange),10)
  eqRecherche = np.poly1d(fastResearch)
  print("Régression termine, quelle hauteur chercher vous (m) ?")
  cherche = float(input(">>"))
  sample = eqRecherche(cherche)
  print("Nous vous proposons une vitesse de ",sample,"tour / seconde")
  print("Qui vous donnerait")
  s = simulation.Simulation(bladeGeom,I,0.01)
  s.simulate(sample*2*np.pi,m)
  ymax,tmax = s.analyseSimulation(True)
  s.simulationGraph()
  erreur = abs(ymax-cherche)/cherche*100
  print("\n le resultat a un taux d erreur de ",erreur,"%\nnous nous excusons pour le resultat imprecis, une nouvelle version du programme fera des recherches plus precises")
  plt.show()


def dispatch():
  c = input("""
Que voulez vous faire ?
Appuyez sur
1 si vous chercher la hauteur a partir de la vitesse de l helice
2 si vous chercher la vitesse de l'helice pour une hauteur (beta)
>>""")
  if(c=="1"):
    handleManual()
  else:
    handleSearch()


dispatch()
