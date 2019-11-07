import math
import matplotlib.pyplot as plt
import numpy as np
import propeller

class Simulation:
  """docstring for Simulation"""
  def __init__(self,bladeGeom,I,end=80,step=0.1):
    super(Simulation, self).__init__()
    self.m = 0
    self.I = I
    self.end = end
    self.bladeGeom = bladeGeom
    self.g = 9.81
    self.D = 0.001
    self.mg = 0
    self.step = step
    self.w0 = 0
    self.t = np.arange(0, self.end, self.step)
    self.v = np.empty_like(self.t)
    self.w = np.empty_like(self.t)
    self.y = np.empty_like(self.t)
    self.a = np.empty_like(self.t)
    self.yByFit = []
    self.vByFit = []
    self.aByFit = []
    self.humanEqY = []
    self.maxiY = 0
    self.Tmax = 0
    self.dureeMontee = 0
    self.dureeDescente = 0
  def L(self,v):
    return(abs(self.D*v**2))
  def arrayToFunc(self,coefs):
    r = ""
    degre = len(coefs)-1
    for i,d in enumerate(reversed(range(degre))):
      r+=str(coefs[i])+"x^"+str(d+1)+" + "
      r += " "+str(coefs[-1])
    return(r)
  def analyseSimulation(self,needToPrint=False):
    t,y = self.t,self.y
    maxiIndex = np.argmax(y)
    maxiY = y[maxiIndex]
    Tmax = t[maxiIndex]
    dureeMontee = Tmax
    dureeDescente = t[-1]-Tmax
    self.maxiY,self.Tmax,self.dureeMontee,self.dureeDescente = maxiY,Tmax,dureeMontee,dureeDescente
    if needToPrint:
      print("----------Analyse --------------")
      print("Hauteur max [m]:",maxiY)
      print("Temps au maximum [s]:",Tmax)
      print("Duree montee [s]",dureeMontee)
      print("Duree descente [s]",dureeDescente)
    return(maxiY,Tmax)
  def analysePlots(self,t,yByFit,vByFit,aByFit):
    plt.figure(1)
    plt.subplot(3,1,1)
    plt.title("Donnees par regression polynomiale ")
    plt.plot(t,yByFit, label="y [m]")
    plt.xlabel('Position en Y en fonction du temps en seconde')
    plt.legend()
    plt.subplot(3,1,2)
    plt.plot(t,vByFit, label="v (en y) m/s")
    plt.xlabel('vitesse en Y en fonction du temps en seconde (dérivée de Y)')
    plt.legend()
    plt.subplot(3,1,3)
    plt.plot(t,aByFit, label="a (en y) [m/s²]")
    plt.xlabel('acceleration en Y en fonction du temps en seconde (dérivée de A)')
    plt.legend()

  def SimulationToPolynomial(self,graph=False):
    t,y = self.t,self.y
    humanEqY = np.polyfit(t,y,3)
    eqYFit = np.polyfit(t,y,20)
    eqYPolynomial = np.poly1d(eqYFit)
    eqVPolynomial = np.polyder(eqYPolynomial)
    eqAPolynomial = np.polyder(eqVPolynomial)
    yByFit = []
    vByFit = []
    aByFit = []
    for i in range(len(t)):
      yByFit.append(eqYPolynomial(t[i]))
      vByFit.append(eqVPolynomial(t[i]))
      aByFit.append(eqAPolynomial(t[i]))
    if graph:
      self.analysePlots(t,yByFit,vByFit,aByFit)
    self.yByFit,self.vByFit,self.aByFit,self.humanEqY = yByFit,vByFit,aByFit,humanEqY
    print("Fonction polynomiale de la hauteur en fonction du temps entre [0 - "+str(t[-1])+"]:",self.arrayToFunc(humanEqY))

  def simulationGraph(self):
    t,y,v,w,a = self.t,self.y,self.v,self.w,self.a
    plt.figure(2)
    plt.subplot(4,1,1)
    plt.title("Donnees par simulation")
    plt.plot(t,y, label="y [m]")
    plt.xlabel('Position en Y en fonction du temps en seconde')
    plt.legend()
    plt.subplot(4,1,2)
    plt.plot(t,v, label="v (en y) m/s")
    plt.xlabel('vitesse en Y en fonction du temps en seconde')
    plt.legend()
    plt.subplot(4,1,3)
    plt.plot(t,a, label="a (en y) [m/s²]")
    plt.xlabel('acceleration en Y en fonction du temps en seconde')
    plt.legend()
    plt.subplot(4,1,4)
    plt.plot(t,w, label="w [rad/s]")
    plt.xlabel('vitesse radiale en fonction du temps en seconde')
    plt.legend()

  def simulate(self,w0,m):
    self.m = m
    self.mg = self.m * self.g
    self.w0 = w0
    self.v[0]=0
    self.y[0]=0
    self.w[0]= w0
    self.a[0]=0
    for i in range(len(self.t)-1):
      dt = self.step
      if(self.y[i] < 0 and i > 0):
        self.t = self.t[0:i]
        self.v = self.v[0:i]
        self.w = self.w[0:i]
        self.y = self.y[0:i]
        self.a = self.a[0:i]
        break
      T,Q =propeller.thrustTorque(self.w[i],self.v[i],3,self.bladeGeom)
      self.a[i] = (T-(self.mg+self.L(self.v[i])))/self.m
      self.y[i+1] = self.y[i] +self.v[i]*dt+ (self.a[i]*dt**2)/2
      self.v[i+1] = self.v[i]  + self.a[i]*dt
      self.w[i+1] = self.w[i]  -(Q/self.I)*dt
# g = 9.81
# m = 0.027
# I = 0.5*0.027*0.0875**2
# bladeGeom = np.array([[0.0135, np.pi/9, 0.025], [0.0730, np.pi/9, 0.039]])
# D=0.001
# w0 = 60*2*np.pi
# si = Simulation(m,bladeGeom,I,w0,0.1)
# si.simulate()
# si.simulationGraph()
# si.analyseSimulation(True)
# si.SimulationToPolynomial(True)
# plt.show()