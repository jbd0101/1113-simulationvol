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

def askCharge():
  try:
    charge = int(input("La charge a transporter (en g) > "))
  except Exception as e:
    charge = 0
  charge = charge/1000.0
  return(charge)
def handleManual():
  w0 = int(input("Vitesse en tour/seconde de l'helice > "))

  mVol = askCharge() + m
  w0 = w0*2*np.pi
  vol.simulate(w0,mVol)
  vol.simulationGraph()
  vol.analyseSimulation(True)
  vol.SimulationToPolynomial(True)
  plt.show()

handleManual()
