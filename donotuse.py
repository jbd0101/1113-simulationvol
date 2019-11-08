# import math
# import matplotlib.pyplot as plt
# import numpy as np
# import propeller

# g = 9.81
# m = 0.027
# mg = g*m

# I = 0.5*0.027*0.0875**2
# bladeGeom = np.array([[0.0135, np.pi/9, 0.025], [0.0730, np.pi/9, 0.039]])
# D=0.001

# step = 0.1     # pas (dt) [s]
# end = 80       # durée [s] max le programme s'arrete si y<0

# t = np.arange(0, end, step)
# v = np.empty_like(t)
# w = np.empty_like(t)
# y = np.empty_like(t)
# a = np.empty_like(t)
# print("------------ BIENVENUE AU SIMULATEUR DU GROUPE 11.13 -------------- \n")
# print("------------     Donnees de base non modifiable     -------------- \n\n")
# print("Duree max du vol autorise (protection anti con pour les intimes): ",end,"s")
# print("Par step de : ",step,"s")
# print("une inertie de: ",I,"kg.m² elle est balaise hein :p")
# print("Avec une gravite de: ",g,"m/s² bravo l'originialite groupe 11.13")
# print("Bref après ces messages inutiles, que vous ne lirez pas, veuillez entrer:\n\n ")

# v0 = int(input("Vitesse en tour/seconde de l'helice > "))
# v0 = v0*2*np.pi

# def L(v):
#   return abs((D*v**2))

# def simulation(v0):
#   global a,v,w,y,t
#   v[0]=0
#   y[0]=0
#   w[0]=v0
#   a[0]=0
#   for i in range(len(t)-1):
#     dt = step
#     if(y[i] < 0 and i > 0):
#       t = t[0:i]
#       v = v[0:i]
#       w = w[0:i]
#       y = y[0:i]
#       a = a[0:i]
#       break
#     T,Q =propeller.thrustTorque(w[i],v[i],3,bladeGeom)
#     a[i] = (T-(mg+L(v[i])))/m
#     y[i+1] = y[i] + v[i]*dt +a[i]*(dt**2)/2
#     v[i+1] = v[i] + a[i]*dt
#     w[i+1] = w[i] - (Q/I)*dt
#     print("T:{0} | Q: {1} |a {2} | v {4} | w {3} ".format(T,Q,a[i],w[i],v[i]))

# def arrayToFunc(coefs):
#   r = ""
#   degre = len(coefs)-1
#   for i,d in enumerate(reversed(range(degre))):
#     r+=str(coefs[i])+"x^"+str(d+1)+" + "
#   r += " "+str(coefs[-1])
#   return(r)
# def analyseSimulation():
#   maxiIndex = np.argmax(y)
#   maxiY = y[maxiIndex]
#   Tmax = t[maxiIndex]
#   dureeMontee = Tmax
#   dureeDescente = t[-1]-Tmax
#   eqYFit = np.polyfit(t,y,20)
#   humanEqY = np.polyfit(t,y,3)
#   eqYPolynomial = np.poly1d(eqYFit)
#   eqVPolynomial = np.polyder(eqYPolynomial)
#   eqAPolynomial = np.polyder(eqVPolynomial)
#   yByFit = []
#   vByFit = []
#   aByFit = []
#   for i in range(len(t)):
#     yByFit.append(eqYPolynomial(t[i]))
#     vByFit.append(eqVPolynomial(t[i]))
#     aByFit.append(eqAPolynomial(t[i]))
#   analysePlots(t,yByFit,vByFit,aByFit)
#   print("----------Analyse --------------")
#   print("Hauteur max [m]:",maxiY)
#   print("Temps au maximum [s]:",Tmax)
#   print("Duree montee [s]",dureeMontee)
#   print("Duree descente [s]",dureeDescente)
#   print("Fonction polynomiale de la hauteur en fonction du temps entre [0 - "+str(t[-1])+"]:",arrayToFunc(humanEqY))

# def analysePlots(t,yByFit,vByFit,aByFit):
#   plt.figure(1)
#   plt.subplot(3,1,1)
#   plt.title("Donnees par regression polynomiale ")
#   plt.plot(t,yByFit, label="y [m]")
#   plt.xlabel('Position en Y en fonction du temps en seconde')
#   plt.legend()
#   plt.subplot(3,1,2)
#   plt.plot(t,vByFit, label="v (en y) m/s")
#   plt.xlabel('vitesse en Y en fonction du temps en seconde (dérivée de Y)')
#   plt.legend()
#   plt.subplot(3,1,3)
#   plt.plot(t,aByFit, label="a (en y) [m/s²]")
#   plt.xlabel('acceleration en Y en fonction du temps en seconde (dérivée de A)')
#   plt.legend()

#   plt.legend()

# def simulationPlots():
#   plt.figure(2)
#   plt.subplot(4,1,1)
#   plt.title("Donnees par simulation")
#   plt.plot(t,y, label="y [m]")
#   plt.xlabel('Position en Y en fonction du temps en seconde')
#   plt.legend()
#   plt.subplot(4,1,2)
#   plt.plot(t,v, label="v (en y) m/s")
#   plt.xlabel('vitesse en Y en fonction du temps en seconde')
#   plt.legend()
#   plt.subplot(4,1,3)
#   plt.plot(t,a, label="a (en y) [m/s²]")
#   plt.xlabel('acceleration en Y en fonction du temps en seconde')
#   plt.legend()
#   plt.subplot(4,1,4)
#   plt.plot(t,w, label="w [rad/s]")
#   plt.xlabel('vitesse radiale en fonction du temps en seconde')

#   plt.legend()
#   plt.show()


# simulation(v0)
# analyseSimulation()
# simulationPlots()
