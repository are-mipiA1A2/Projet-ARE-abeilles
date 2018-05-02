import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as anim
import random

N=100 #taille de la région étudiée (côté en m, donc 1 hectare)

def simulation(Liste_guepes):
    global h
    global jour
    global N
    global Liste_ruches
    global Nb_recoltes
    global Info_ruches
    global taux_nat
    global taux_mort
    global saison
    global Nb_ruches
    global taux_pol
    global Nb_zones
    global Liste_Nb_abeilles_tot
    global Guepe
    global Frelon
    global Nb_zones_fleur
    global liste_zone_fleur


    Nb_zone_fleur= 120 #nombre de zones florales
    liste_zone_fleur=[] #liste des coordonnées des zones florales
    while len(liste_zone_fleur)<Nb_zone_fleur:
        x1=random.randint(0,N-1)
        y1=random.randint(0,N-1)
        if (x1,y1) not in liste_zone_fleur:
            liste_zone_fleur.append((x1,y1))
    
    Nb_ruches=4 #nombre de  ruches
    Liste_ruches=[] #liste des coordonnées de chaque rûche
    while len(Liste_ruches)!=Nb_ruches:
        x0=random.randint(0,N-1)
        y0=random.randint(0,N-1)             #coordonnées de la rûche
        if (x0,y0) not in Liste_ruches and (x0,y0) not in liste_zone_fleur and (x0,y0) not in Liste_guepes:
            Liste_ruches.append((x0,y0))


    Info_ruches=[] #Toutes les informations sur chaque ruche
    Nb_abeilles=12000 #nombre initial d'abeilles dans la ruche
    reperage=0 #nombre de zones florales découvertes
    liste_reper=[] #liste des zones florales découvertes
    distance=0 #distance initiale du repérage par rapport à la ruche
    Nb_zones=8 #nombre de zones florales à découvrir
    Arrivée=0 #0 signifie que les butineuses partent, 1 qu'elles butinent et 2 qu'elles rentrent à la rûche et 3 qu'elles sont dans la rûche
    qtt_miel=10000000 #qantité de miel dans la rûche en mg
    taux_mort=41 #nombre de décès en une heure (naturellement), obtenu en divisant l'espérance de vie d'une abeille par le nombre d'abeilles
    Liste_direct=[] #Liste des directions à prendre pour aller vers une fleur
    parasitage=0 # 0: non infectée, 1: infectée, 2: gravement infectée
    essaimage=0 # 0: ruche normale ; 1: duplication ; 2: migration
    for i in Liste_ruches:
        x0,y0=i
        age_reine=random.randint(0,1094) #une reine peut vivre jusqu'à 3 ans
        esperance_reine=random.randint(1095,1460)
        Info_ruches.append((x0,y0,Nb_abeilles,reperage,liste_reper,distance,Liste_direct,qtt_miel,parasitage,essaimage,age_reine,esperance_reine))
    nb_steps=91*24*8 #nombre d'heures écoulées

    taux_nat=63 #nombre de naissances en une heure
    h=0 #nombre d'heures écoulées
    jour=0 #nombre de jours écoulés
    saison='printemps' #saison de départ
    Nb_recoltes=0 #Nb de récoltes effectuées dans la journée
    Nb_abeilles_tot=Nb_ruches*Nb_abeilles #nombre total d'abeilles dans la région
    Liste_Nb_abeilles_tot=[Nb_abeilles_tot]
    Liste_qtt_miel_tot=[qtt_miel*Nb_ruches]
    taux_pol=0


    for i in range(nb_steps):
        Nb_abeilles_tot=0
        qtt_miel_tot=0
        h=h+1

        if h==24: #une journée écoulée
            jour=jour+1
            Nb_recoltes=0
            h=0
            if jour==91: #une saison écoulée
                Ab_tot=Liste_Nb_abeilles_tot[i-1]
                if saison=='printemps':
                    taux_nat=25
                    saison='été'
                elif saison=='été':
                    saison='automne'
                    taux_mort=29
                elif saison=='automne':
                    taux_nat=27
                    saison='hiver'
                elif saison=='hiver':
                    taux_nat=63
                    saison='printemps'
                    taux_mort=41
                jour=0

        if saison=='été' and jour==0 and h==0:
            k=random.randint(18,78)
            infection=int(k*Nb_ruches/100)
            Liste_infect=[] #liste des coordonnées des ruches infectée par des parasites
            while len(Liste_infect)!= infection:
                i=random.randint(0,Nb_ruches-1)
                if Liste_ruches[i] not in Liste_infect:
                    Liste_infect.append(Liste_ruches[i])

        if saison=='été' and h==0 and jour==45:
            k=random.randint(18,78)
            infection=int(k*Nb_ruches/100)
            Liste_infect=[] #liste des coordonnées des ruches infectée par des parasites
            while len(Liste_infect)!= infection:
                i=random.randint(0,Nb_ruches-1)
                if Liste_ruches[i] not in Liste_infect:
                    Liste_infect.append(Liste_ruches[i])
        
        Info_ruches_copy=[]
        for k in Info_ruches:
            x0,y0,Nb_abeilles,reperage,liste_reper,distance,Liste_direct,qtt_miel,parasitage,essaimage,age_reine,esperance_reine=k
    
            if h==0: #vieillissement de la reine
                age_reine=age_reine+1
                if age_reine==esperance_reine: #mort et naissance de reines
                    age_reine=0
                    esperance_reine=random.randint(1095,1460)
                    if saison=='hiver':
                        essaimage=2

            if saison!='hiver': #attaque de guêpes (probable à chaque heure)
                attaque=random.randint(0,140)
                if attaque==1 and Frelon+Guepe>0:
                    escouade=np.random.choice(5) # escouade de 1 à 5 guêpes
                    espece=random.randint(0,Guepe+Frelon-1)
                    gardiennes=int(Nb_abeilles/4)
                    if espece<=Guepe: #escouade de guêpes
                        Nb_abeilles=Nb_abeilles-2*escouade
                    else: #escouade de frelons
                        if 40-int(gardiennes/1000)>0:
                            Nb_abeilles=Nb_abeilles-(40-int(gardiennes/1000))*100*escouade
                        else:
                            Nb_abeilles=Nb_abeilles-40*escouade
                    if Nb_abeilles<0:
                        Nb_abeilles=0
                
            if saison=='été' and j==0 and h==0:
                if (x0,y0) in Liste_infect:
                    parasitage=1           

            if saison=='été' and h==0 and j==45:
                if (x0,y0) in Liste_infect and parasitage==0:
                    parasitage=1
                if (x0,y0) in Liste_infect and parasitage==1:
                    parasitage=2
                
            if saison=='automne' and h==0 and j==0:
                parasitage=0 

            if essaimage==1 and saison=='printemps' and jour==0:
                place_indispo=set() #permet de vérifer s'il y a de la place pour une nouvelle ruche
                for k in Liste_ruches:
                    x,y=k
                    place_indispo.add((x,y))
                for k in liste_zone_fleur:
                    x,y=k
                    place_indispo.add((x,y))
                for k in Liste_guepes:
                    x,y,_=k
                    place_indispo.add((x,y))
                if len(place_indispo)<N**2:
                    Nb_ruches=Nb_ruches+1
                    while len(Info_ruches)<Nb_ruches:
                        x=np.random.choice(N)
                        x = x % N
                        y=np.random.choice(N)
                        y = y % N              #coordonnées de la rûche
                        if (x,y) not in place_indispo:
                            Liste_ruches.append((x,y))
                            Info_ruches.append((x,y,int(Nb_abeilles/2),0,[],0,[],int(qtt_miel/2),parasitage,0,age_reine,esperance_reine))
                    Nb_abeilles=Nb_abeilles-int(Nb_abeilles/2)
                    qtt_miel=qtt_miel-int(qtt_miel/2)
                    essaimage=0
                    age_reine=1
                    esperance_reine=random.randint(1095,1460)
                else:
                    essaimage=3

            if essaimage==2:
                place_indispo=set() #permet de vérifer s'il y a de la place pour une nouvelle ruche
                for k in Liste_ruches:
                    x,y=k
                    place_indispo.add((x,y))
                for k in liste_zone_fleur:
                    x,y=k
                    place_indispo.add((x,y))
                for k in Liste_guepes:
                    x,y,_=k
                    place_indispo.add((x,y))
                if len(place_indispo)<N**2:
                    Liste_ruches_copy=[]
                    x=np.random.choice(N)
                    x = x % N
                    y=np.random.choice(N)
                    y = y % N              #coordonnées de la rûche
                    while (x,y) in place_indispo:
                        x=np.random.choice(N)
                        x = x % N
                        y=np.random.choice(N)
                        y = y % N              #coordonnées de la rûche
                    for k in Liste_ruches:
                        x1,y1=k
                        if x1==x0 and y1==y0:
                            Liste_ruches_copy.append((x,y))
                        else:
                            Liste_ruches_copy.append((x1,y1))
                    Liste_ruches=Liste_ruches_copy.copy()
                    x0=x
                    y0=y
                    reperage=0
                    liste_reper=[]
                    distance=0
                    essaimage=0
                    
                else:
                    essaimage=3

            
            if h==16: #Au bout d'un certain temps, les abeilles vont consommer le miel
                if qtt_miel-3*Nb_abeilles-14000<0: # 3 mg mangés par chaque abeille, 14g utilisés pour la production de cire
                    if qtt_miel-3*Nb_abeilles<0:
                        Nb_abeilles=int(qtt_miel/3)
                    qtt_miel=0
                else:
                    qtt_miel=qtt_miel-3*Nb_abeilles-14000 
                

            #mort d'une abeille naturelle
            Nb_abeilles=Nb_abeilles-taux_mort
            if Nb_abeilles<0:
                Nb_abeilles=0

            #mort des abeilles à cause de l'homme
            if h==23:
                Nb_abeilles=Nb_abeilles-taux_pol*reperage
                if Nb_abeilles<0:
                    Nb_abeilles=0

            
            if essaimage!=2: #naissance d'une abeille
                Nb_abeilles=Nb_abeilles+taux_nat
                if saison=='hiver':
                    r=random.randint(0,1)
                    if r==1:
                        Nb_abeilles=Nb_abeilles+1

                                  
            if reperage<Nb_zones:
                liste_repera=liste_reper.copy()
                distance=distance+1
                for j in range(-distance,distance+1):
                    for k in range(-distance,distance+1):               #zone de repérage carrée autour de la ruche
                        if j==-distance or j==distance or k==-distance or k==distance: #zone encore inexplorée
                            if (j+x0,k+y0) in liste_zone_fleur:
                                reperage=reperage+1
                                liste_repera.append((j+x0,k+y0))
                liste_reper=liste_repera.copy()
                
            if reperage>=Nb_zones and Nb_recoltes<10:
                T_groupe=int(int(Nb_abeilles/2)/reperage) #nombre d'abeilles dans un groupe (les butineuses représentent la moitié de la ruche)
                Liste_direct=[] #liste des directions pour chaque groupe
                for k in range(reperage):
                    Liste_direct.append(((x0,y0),liste_reper[k],T_groupe)) #coordonnées du groupe, de sa destination, son nombre de membres
                    Nb_abeilles=Nb_abeilles-T_groupe
                
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b), (c,d), T_groupe= k
                    while (a,b)!=(c,d):
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
                        if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                            T_groupe=T_groupe-2
                            if T_groupe<0:
                                T_groupe=0
                        if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                            T_groupe=T_groupe-25
                            if T_groupe<0:
                                T_groupe=0
                    Liste_dir.append(((a,b),(c,d),T_groupe))
                Liste_direct=Liste_dir.copy()
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b),(c,d),T_groupe=k
                    crabe_araignée=random.randint(1,150) #probabilité qu'un crabe araignée se situe dans cette zone et mange une abeille
                    if crabe_araignée==50:
                        T_groupe=T_groupe-1
                        if T_groupe<=0:
                            T_groupe=0
                    Liste_dir.append(((a,b),(c,d),T_groupe))
                Liste_direct=Liste_dir.copy()
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b),_,T_groupe=k
                    if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                        T_groupe=T_groupe-2*300
                        if T_groupe<=0:
                            T_groupe=0
                    if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                        T_groupe=T_groupe-25*300
                        if T_groupe<=0:
                            T_groupe=0
                    Liste_dir.append(((a,b),(x0,y0),T_groupe))
                Liste_direct=Liste_dir.copy()
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b), (c,d),T_groupe= k
                    while (a,b)!=(c,d):
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
                        if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                            T_groupe=T_groupe-2
                            if T_groupe<0:
                                T_groupe=0
                        if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                            T_groupe=T_groupe-25
                            if T_groupe<0:
                                T_groupe=0
                    Liste_dir.append(((a,b),(c,d),T_groupe))
                Liste_direct=Liste_dir.copy()
                Liste_dir=[]
                for k in Liste_direct:
                    (a,b),(c,d),T_groupe=k
                    Nb_abeilles=Nb_abeilles+T_groupe
                    qtt_miel=qtt_miel+(13-taux_pol)*T_groupe #chaque abeille ramène 13 mg de miel
                    if parasitage==1:
                        qtt_miel=qtt_miel-(3296-329*taux_pol) #3kg de miel perdus en été  avec parasitage de lvl 1
                    if parasitage==2:
                        qtt_miel=qtt_miel-(6593-659*taux_pol) #6kg de miel perdus en été  avec parasitage de lvl 2
                    if qtt_miel>30000000: #capacité de miel maximum dans une rûche en mg
                        essaimage=1
                        qtt_miel=30000000
                    if qtt_miel<0:
                        qtt_miel=0
                    Liste_dir.append(((a,b),(c,d),0))
                Liste_direct=Liste_dir.copy()
                Nb_recoltes=Nb_recoltes+1

                
            """print((x0,y0,Nb_abeilles,reperage,liste_reper.copy(),distance,Liste_direct.copy(),qtt_miel,parasitage),'\n',s)"""
            #vérification de dernier recours en cas de bug redoutable
            """print(Nb_abeilles,h)""" #vérification rapide en cas de bug majeur
            Info_ruches_copy.append((x0,y0,Nb_abeilles,reperage,liste_reper.copy(),distance,Liste_direct.copy(),qtt_miel,parasitage,essaimage,age_reine,esperance_reine))
            Nb_abeilles_tot=Nb_abeilles_tot+Nb_abeilles
            qtt_miel_tot=qtt_miel_tot+qtt_miel
        Liste_qtt_miel_tot.append(qtt_miel_tot)
        Liste_Nb_abeilles_tot.append(Nb_abeilles_tot)
        Info_ruches=Info_ruches_copy.copy()
    
        
        """terrain=np.zeros([N,N])
        for a in range(N):
            for b in range(N):
                    for k in Info_ruches:
                        x0,y0,Nb_abeilles,_,_,_,Liste_direct,_,_,_,_,_=k
                        if (a,b)==(x0,y0):
                            terrain[a][b]=terrain[a][b]+Nb_abeilles
                        for i in Liste_direct:
                            (c,d),_,T_groupe=i
                            if (c,d)==(a,b):
                                terrain[a][b]=terrain[a][b]+T_groupe
                                
        results.append(terrain.copy())"""
    return(Liste_Nb_abeilles_tot,Nb_ruches,Liste_qtt_miel_tot)
 

y=[]
Liste_guepes=[]
for i in range(0,6):
    print(i)
    #Création des zones habitées par des prédateurs
    Guepe=2*i #nombre de nids de guêpe
    Frelon=i #nombre de nids de frelon
    Liste_guepes[:]=[]
    while len(Liste_guepes)!=Guepe:
        x0=random.randint(0,N-1)
        y0=random.randint(0,N-1)           #coordonnées du nid de guepes
        if (x0,y0) not in Liste_guepes:
            Liste_guepes.append((x0,y0,1))
    while len(Liste_guepes)!=Frelon+Guepe:
        x0=random.randint(0,N-1)
        y0=random.randint(0,N-1)             #coordonnées du nid de frelons
        if (x0,y0) not in Liste_guepes:
            Liste_guepes.append((x0,y0,2))
    Abeilles,_,_=simulation(Liste_guepes)
    AB=Abeilles.copy()
    k=AB[91*24*5]
    Abeilles[:]=[]
    y.append(k)


x=[i for i in range(0,6)]

"""for i in range(len(results)):
    print(results[i],'\n',i)""" #vérification assez rapide pour détecter de potentiels bugs

plt.title("Nombre d'abeilles selon la prédation")
plt.plot(x,y,"r")
plt.xlabel("Taux de prédation")
plt.ylabel("Abeilles")
plt.show()
