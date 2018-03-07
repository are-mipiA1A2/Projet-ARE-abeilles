import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as anim

N=100 #taille de la région étudiée (en m**2)
nb_steps=1000 #nombre d'images total
x=np.random.choice(N)
x1 = x % N
y=np.random.choice(N)
y1 = y % N
x=np.random.choice(N)
x2 = x % N
y=np.random.choice(N)
y2 = y % N
x=np.random.choice(N)
x3 = x % N
y=np.random.choice(N)
y3 = y % N
liste_zone_fleur=[(x1,y1),(x2,y2),(x3,y3)] #liste des coordonnées des zones florales
Nb_abeilles=5000 #nombre initial d'abeilles dans la ruche
taux_nat=217 #nombre de secondes avant une naissance
s=0 #nombre de secondes écoulées modulo taux_nat
Nb_butineuses=abs(Nb_abeilles/2)
reperage=0 #nombre de zones florales découvertes
liste_reper=[] #liste des zones florales découvertes
distance=0 #distance initiale du repérage par rapport à la ruche
Nb_zones=3 #nombre de zones florales à découvrir
Nb_but_dehors=0 #nombre de butineuses hors de la ruche
Nb_ab_dedans=Nb_abeilles

terrain=np.zeros([N,N])

x=np.random.choice(N)
x0 = x % N
y=np.random.choice(N)
y0 = y % N
terrain[x0][y0]=Nb_abeilles

results=[]
results.append(terrain.copy())

def simulation():
    global Nb_groupes
    global T_groupe
    global Liste_direct
    global s
    global reperage
    global distance
    global Nb_but_dehors
    global Nb_abeilles
    global Nb_ab_dedans

    for i in range(nb_steps):
        s=s+1
        if s==taux_nat:                 #naissance d'une abeille
            s=0
            Nb_abeilles=Nb_abeilles+1
            Nb_ab_dedans=Nb_ab_dedans+1
            terrain[x0][y0]=Nb_ab_dedans
        if reperage<Nb_zones:
            distance=distance+1
            for j in range(-distance,distance+1):
                for k in range(-distance,distance+1):               #zone de repérage carrée autour de la ruche
                    if j==-distance or j==distance or k==-distance or k==distance: #zone encore inexplorée
                        if (j+x0,k+y0) in liste_zone_fleur:
                            reperage=reperage+1
                            liste_reper.append((j+x0,k+y0))
        if reperage>=Nb_zones:
            
            if Nb_but_dehors==0:
                Nb_groupes=reperage #nombre de groupe de butineuses
                T_groupe=abs(Nb_butineuses/Nb_groupes) #nombre d'abeilles dans un groupe
                Liste_direct=[] #liste des directions pour chaque groupe
                for k in range(Nb_groupes):
                    Liste_direct.append(((x0,y0),liste_reper[k]))
                Nb_but_dehors=Nb_butineuses
                Nb_ab_dedans=Nb_ab_dedans-Nb_but_dehors
                
            elif Nb_but_dehors!=0:
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b), (c,d)= k
                    if (a,b)!=(c,d):
                        terrain[a][b]=terrain[a][b]-T_groupe
                        action=0
                        while action!=2 and (a,b)!=(c,d):
                            if abs(a-c)>abs(b-d):
                                if a-c>0:
                                    a=a-1
                                elif a-c<0:
                                    a=a+1
                            elif abs(a-c)<abs(b-d):
                                if b-d>0:
                                    b=b-1
                                elif b-d<0:
                                    b=b+1
                            elif abs(a-c)==abs(b-d):
                                if a-c<0 and b-d<0:
                                    a=a+1
                                    b=b+1
                                elif a-c<0 and b-d>0:
                                    a=a+1
                                    b=b-1
                                elif a-c>0 and b-d>0:
                                    a=a-1
                                    b=b-1
                                elif a-c>0 and b-d<0:
                                    a=a-1
                                    b=b+1
                            action=action+1
                        terrain[a][b]=terrain[a][b]+T_groupe
                        Liste_dir.append(((a,b),(c,d)))
                Liste_direct=Liste_dir.copy()
                    
        
        results.append(terrain.copy())
    return(results)
 
results=simulation()

        
fig = plt.figure()

# results[i] contient l'état au pas de temps i sous forme de matrice
im = plt.imshow(results[0], animated=True)

def updatefig(i):

    im.set_array(results[i+1])
    
    return im,

ani = anim.FuncAnimation(fig, updatefig, frames=1000, interval=50, blit=True)

plt.show()
