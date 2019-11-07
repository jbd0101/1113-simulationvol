#
# Simulation: un bloc attaché à un ressort sur un sol plat
#
# Charles Pecheur 2018
#

import math
import matplotlib.pyplot as plt
import numpy as np

### Constantes

g = 9.81         # gravitation [m/s**2]

### Paramètres du système

m = 0.1          # masse du bloc [kg]
mu = 0.03        # coefficient de frottement visqueux [N*s/m]
k = 0.5          # coefficient du ressort [N/m]

### Paramètres de la simulation

step = 0.001     # pas (dt) [s]
end = 20.0       # durée [s]
x_0 = -5.0       # position initiale [m]
v_0 = 0.0        # vitesse initiale [m/s]

t = np.arange(0, end, step)
x = np.empty_like(t)          
v = np.empty_like(t)
a = np.empty_like(t)
    
def simulation():
    """
    pre: -
    post: exécute une simulation jusqu'à t=end par pas de dt=step.
          Remplit les listes x, v, a des positions, vitesses et accélérations.
    """
    # conditions initiales
    x[0] = x_0
    v[0] = v_0
    
    for i in range(len(t)-1):

        dt = step
        
        # calcul de la force totale
        f_ressort = -k * x[i]
        f_frott = -mu * v[i]
        f_tot = f_ressort + f_frott
        
        # calcul accélération, vitesse, position
        a[i] = f_tot / m
        v[i+1] = v[i] + a[i] * dt
        x[i+1] = x[i] + v[i] * dt
        a[i+1] = a[i]

def graphiques():
    
    plt.figure(1)
    plt.subplot(3,1,1)
    plt.plot(t,x, label="x")
    plt.legend()
    plt.subplot(3,1,2)
    plt.plot(t,v, label="v")
    plt.legend()
    plt.subplot(3,1,3)
    plt.plot(t,a, label="a")
    plt.legend()
    plt.show()

def graphiques_energie():
    e_ressort = np.empty_like(t)
    e_cin = np.empty_like(t)
    e_tot = np.empty_like(t)
    for i in range(len(t)):
        e_ressort[i] = k * x[i]**2 / 2
        e_cin[i] = m * v[i]**2 / 2
        e_tot[i] = e_ressort[i] + e_cin[i]

    plt.figure(2)
    plt.plot(t, e_ressort, label="ressort")
    plt.plot(t, e_cin, label="cinétique")
    plt.plot(t, e_tot, label="total")
    plt.legend()
    plt.show()

### programme principal

simulation()
graphiques()
graphiques_energie()

mu = 0.1
x_0 = +10.0
simulation()
graphiques()
graphiques_energie()

