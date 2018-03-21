import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as anim

N=70 #nb d'abeille au départ
nb_steps=2000 #nb de seconde en tout
taux_nat=217 #une abeille nait toute les 217 secondes


def naissancex(n):
    """nb d'abeille qui nait"""
    x=1
    y=N
    LRx=[]
    LRy=[]
    for n in range(1,n+1):
        if n%taux_nat==0:
            x=n
            y=y+1
            LRx.append(x)
    
    return LRx

assert naissancex(434)==([217, 434])

def naissancey(n):
    """nb d'abeille qui nait"""
    x=1
    y=N
    LRx=[]
    LRy=[]
    for n in range(1,n+1):
        if n%taux_nat==0:
            x=n
            y=y+1
            LRy.append(y)
    
    return LRy

assert naissancey(434)==([71, 72])

x=naissancex(nb_steps)
y=naissancey(nb_steps)
plt.title("Evolution du nombre d'abeille par seconde")
plt.plot(x,y,"r")
plt.xlabel('Temps')
plt.ylabel("nombre d'abeille")
plt.show()


