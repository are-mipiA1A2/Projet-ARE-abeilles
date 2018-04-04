import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as anim

N=100 #taille de la région étudiée (côté en m, donc 1 hectare)
Nb_ruches=4 #nombre de  ruches
Liste_ruches=[] #liste des coordonnées de chaque rûche
while len(Liste_ruches)!=Nb_ruches:
    x=np.random.choice(N)
    x0 = x % N
    y=np.random.choice(N)
    y0 = y % N              #coordonnées de la rûche
    if (x0,y0) not in Liste_ruches:
        Liste_ruches.append((x0,y0))

#Création des zones habitées par des prédateurs
Guepe=1 #nombre de nids de guêpe
Frelon=1 #nombre de nids de frelon

Liste_guepes=[]
while len(Liste_guepes)!=Guepe:
    x=np.random.choice(N)
    x0 = x % N
    y=np.random.choice(N)
    y0 = y % N              #coordonnées du nid de guepes
    if (x0,y0) not in Liste_guepes and (x0,y0) not in Liste_ruches:
        Liste_guepes.append((x0,y0,1))
while len(Liste_guepes)!=Frelon+Guepe:
    x=np.random.choice(N)
    x0 = x % N
    y=np.random.choice(N)
    y0 = y % N              #coordonnées du nid de frelons
    if (x0,y0) not in Liste_guepes and (x0,y0) not in Liste_ruches:
        Liste_guepes.append((x0,y0,2))



Info_ruches=[] #Toutes les informations sur chaque ruche
Nb_abeilles=30000 #nombre initial d'abeilles dans la ruche
Nb_ab_dedans=Nb_abeilles #nombre d'abeiles dans la rûche
but_dehors=0  # 0: période de repos, 1: période de récolte
reperage=0 #nombre de zones florales découvertes
liste_reper=[] #liste des zones florales découvertes
distance=0 #distance initiale du repérage par rapport à la ruche
Nb_zones=8 #nombre de zones florales à découvrir
Arrivée=0 #0 signifie que les butineuses partent, 1 qu'elles butinent et 2 qu'elles rentrent à la rûche et 3 qu'elles sont dans la rûche
qtt_miel=10000000 #qantité de miel dans la rûche en mg
taux_mort=121 #nombre de secondes avant la mort d'une abeille (naturellement), obtenu en divisant l'espérance de vie d'une abeille par le nombre d'abeilles
Liste_direct=[] #Liste des directions à prendre pour aller vers une fleur
Temps_recolte_passe=0 #temps réeelement passé par les butineuses sur les fleurs actuellement
parasitage=0 # 0: non infectée, 1: infectée, 2: gravement infectée
essaimage=0 # 0: ruche normale ; 1: duplication ; 2: migration
for i in Liste_ruches:
    x0,y0=i
    age_reine=np.random.choice(1095) #une reine peut vivre jusqu'à 3 ans
    esperance_reine=np.random.choice(1096,1460)
    Info_ruches.append((x0,y0,Nb_abeilles,Nb_ab_dedans,but_dehors,reperage,liste_reper,distance,
                        Arrivée,Liste_direct,Temps_recolte_passe,qtt_miel,parasitage,essaimage,age_reine,esperance_reine))
nb_steps=500 #nombre d'images total
Nb_zone_fleur= 120 #nombre de zones florales
liste_zone_fleur=[] #liste des coordonnées des zones florales
while len(liste_zone_fleur)<Nb_zone_fleur:
    x=np.random.choice(N)
    x1 = x % N
    y=np.random.choice(N)
    y1 = y % N
    if (x1,y1) not in liste_zone_fleur and (x1,y1) not in Liste_ruches:
        liste_zone_fleur.append((x1,y1))
taux_nat=57 #nombre de secondes avant une naissance
s=0 #nombre de secondes écoulées
j=0 #nombre de jours écoulés
saison='printemps' #saison de départ
Temps_interrecolte=3720 # 3720 = nombre de secondes entre chaque récolte
Temps_recolte=600 # 600 = temps à butiner
Nb_abeilles_tot=Nb_ruches*Nb_abeilles #nombre total d'abeilles dans la région
Liste_Nb_abeilles_tot=[Nb_abeilles_tot]




terrain=np.zeros([N,N])

for k in Info_ruches:
    x0,y0,Nb_abeilles,_,_,_,_,_,_,_,_,_,_,_,_,_=k
    terrain[x0][y0]=Nb_abeilles


results=[]
results.append(terrain.copy())

def simulation():
    global s
    global j
    global N
    global Liste_ruches
    global liste_zone_fleur
    global Guepe
    global Frelon
    global Temps_recolte
    global Temps_interrecolte
    global Info_ruches
    global taux_nat
    global taux_mort
    global saison
    global Nb_ruches
    global Liste_guepes
    global Nb_zones

    for i in range(nb_steps):
        Nb_abeilles_tot=0
        s=s+1

        if s==86400: #une journée écoulée
            j=j+1
            s=0
            if j==91: #une saison écoulée
                Ab_tot=Liste_Nb_abeilles_tot[nb_steps-1]
                if saison=='printemps':
                    taux_nat=216
                    saison='été'
                    taux_mort=int(3628800/(AB_tot/Nb_ruches))#esprérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='été':
                    saison='automne'
                    taux_mort=int(17280000/(AB_tot/Nb_ruches)) #esprérance de vie de 200 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='automne':
                    taux_nat=144
                    saison='hiver'
                    taux_mort=int(3628800/(AB_tot/Nb_ruches)) #esprérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                elif saison=='hiver':
                    taux_nat=57
                    saison='printemps'
                    taux_mort=int(3628800/(AB_tot/Nb_ruches)) #espérance de vie de 42 jours par le nombre d'abeilles moyen dans une  ruche
                j=0

        if saison=='été' and j==0 and s==0:
            k=np.random.choice(18,79)
            infection=int(k*Nb_ruches/100)
            Liste_infect=[] #liste des coordonnées des ruches infectée par des parasites
            while len(Liste_infect)!= infection:
                i=np.random.choice(Nb_ruches)
                if Liste_ruches[i] not in Liste_infect:
                    Liste_infect.append(Liste_ruches[i])

        if saison=='été' and s==0 and j==45:
            k=np.random.choice(18,79)
            infection=int(k*Nb_ruches/100)
            Liste_infect=[] #liste des coordonnées des ruches infectée par des parasites
            while len(Liste_infect)!= infection:
                i=np.random.choice(Nb_ruches)
                if Liste_ruches[i] not in Liste_infect:
                    Liste_infect.append(Liste_ruches[i])
        
        Info_ruches_copy=[]
        for k in Info_ruches:
            x0,y0,Nb_abeilles,Nb_ab_dedans,but_dehors,reperage,liste_reper,distance,Arrivée,Liste_direct,Temps_recolte_passe,qtt_miel,parasitage,essaimage,age_reine,esperance_reine=k

            if Nb_abeilles<5000:
                essaimage=2
    
            if s==0: #vieillissement de la reine
                age_reine=age_reine+1
                if age_reine==esperance_reine: #mort et naissance de reines
                    age_reine=0
                    esperance_reine=np.random.choice(1096,1460)
                    if saison=='hiver':
                        essaimage=2

            if s/60==int(s/60) and saison!='hiver': #attaque de guêpes (probable à chaque heure)
                attaque=np.random.choice(35)+1
                if attaque==1 and Frelon+Guepe>0:
                    escouade=np.random.choice(5) # escouade de 1 à 5 guêpes
                    espece=np.random.choice(Guepe+Frelon-1)+1
                    if but_dehors==0:
                        gardiennes=int(Nb_ab_dedans/4)
                    if but_dehors==1:
                        gardiennes=int(Nb_ab_dedans/2)
                    if espece<=Guepe: #escouade de guêpes
                        Nb_ab_dedans=Nb_ab_dedans-2*escouade
                        Nb_abeilles=Nb_abeilles-2*escouade
                    else: #escouade de frelons
                        if 40-int(gardienne/1000)>0:
                            Nb_ab_dedans=Nb_ab_dedans-(40-int(gardienne/1000))*100*esouade
                            Nb_abeilles=Nb_abeilles-(40-int(gardienne/1000))*100*esouade
                        else:
                            Nb_ab_dedans=Nb_ab_dedans-40*escouade
                            Nb_abeilles=Nb_abeilles-40*escouade
                    if Nb_ab_dedans<0:
                        Nb_ab_dedans=0
                    if Nb_abeilles<0:
                        Nb_abeilles=0
                
            if saison=='été' and j==0 and s==0:
                if (x0,y0) in Liste_infect:
                    parasitage=1           

            if saison=='été' and s==0 and j==45:
                if (x0,y0) in Liste_infect and parasitage==0:
                    parasitage=1
                if (x0,y0) in Liste_infect and parasitage==1:
                    parasitage=2
                
            if saison=='automne' and s==0 and j==0:
                parasitage=0 

            if essaimage==1 and but_dehors==0:
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
                            Info_ruches.append((x,y,int(Nb_abeilles/2),int(Nb_ab_dedans/2),0,0,[],0,0,[],0,int(qtt_miel/2),parasitage,0,age_reine,esperance_reine))
                    Nb_abeilles=Nb_abeilles-int(Nb_abeilles/2)
                    Nb_ab_dedans=Nb_ab_dedans-int(Nb_ab_dedans/2)
                    qtt_miel=qtt_miel-int(qtt_miel/2)
                    essaimage=0
                    age_reine=1
                    esperance_reine=np.random.choice(1096,1460)
                else:
                    essaimage=3

            if essaimage==2 and but_dehors==0:
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

            
            if s==60000: #Au bout d'un certain temps, les abeilles vont consommer le miel
                if qtt_miel-3*Nb_abeilles-14000<0: # 3 mg mangés par chaque abeille, 14g utilisés pour la production de cire
                    if qtt_miel-3*Nb_abeilles<0:
                        Nb_ab_dedans=int(qtt_miel/3)
                    qtt_miel=0
                else:
                    qtt_miel=qtt_miel-3*Nb_abeilles-14000 
                

            if s/taux_mort==int(s/taux_mort): #mort d'une abeille naturelle
                Nb_ab_dedans=Nb_ab_dedans-1
                if Nb_ab_dedans<0:
                    Nb_ab_dedans=0
                terrain[x0][y0]=Nb_ab_dedans

            
            if s/taux_nat==int(s/taux_nat) and essaimage!=2:                 #naissance d'une abeille
                Nb_ab_dedans=Nb_ab_dedans+1
                terrain[x0][y0]=Nb_ab_dedans

                                  
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
            if reperage>=Nb_zones:
            
                if but_dehors==0 and Arrivée==0 and s<=43200: #Avant que la moitié de la journée soit écoulée
                    but_dehors=1
                    T_groupe=int(int(Nb_ab_dedans/2)/reperage) #nombre d'abeilles dans un groupe (les butineuses représentent la moitié de la ruche)
                    Liste_direct=[] #liste des directions pour chaque groupe
                    for k in range(reperage):
                        Liste_direct.append(((x0,y0),liste_reper[k],T_groupe)) #coordonnées du groupe, de sa destination, son nombre de membres
                    Nb_ab_dedans=Nb_ab_dedans-int(int(Nb_ab_dedans/2)/reperage)*reperage
                
                elif but_dehors==1:
                    if Arrivée==0:
                        Liste_dir=[]
                        for k in Liste_direct:
                            (a,b), (c,d), T_groupe= k
                            if (a,b)!=(c,d):
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
                                    if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                                        T_groupe=T_groupe-5
                                        if T_groupe<0:
                                            T_groupe=0
                                    if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                                        T_groupe=T_groupe-75
                                        if T_groupe<0:
                                            T_groupe=0
                                Liste_dir.append(((a,b),(c,d),T_groupe))
                            elif (a,b)==(c,d):
                                if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                                    T_groupe=T_groupe-2
                                    if T_groupe<=0:
                                        T_groupe=0
                                if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                                    T_groupe=T_groupe-25
                                    if T_groupe<=0:
                                        T_groupe=0
                                Liste_dir.append(((a,b),(c,d),T_groupe))
                        Liste_direct=Liste_dir.copy()
                        valid=0 #permet de vérifier si toutes les abeilles sont arrivées à destination
                        for k in Liste_direct:
                            (a,b),(c,d),T_groupe=k
                            if (a,b)==(c,d):
                                valid=valid+1
                        if valid == len(Liste_direct):
                            Arrivée=1
                            Liste_dir=[]
                            for k in Liste_direct:
                                (a,b),(c,d),T_groupe=k
                                crabe_araignée=np.random.choice(150) #probabilité qu'un crabe araignée se situe dans cette zone et mange une abeille
                                if crabe_araignée==50:
                                    T_groupe=T_groupe-1
                                    if T_groupe<=0:
                                        T_groupe=0
                                Liste_dir.append(((a,b),(c,d),T_groupe))
                            Liste_direct=Liste_dir.copy()
                                  
                    elif Arrivée==1:
                        Temps_recolte_passe=Temps_recolte_passe+1
                        Liste_dir=[]
                        for k in Liste_direct:
                            (a,b),_,T_groupe=k
                            if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                                T_groupe=T_groupe-2
                                if T_groupe<=0:
                                    T_groupe=0
                            if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                                T_groupe=T_groupe-25
                                if T_groupe<=0:
                                    T_groupe=0
                            Liste_dir.append(((a,b),(x0,y0),T_groupe))
                        Liste_direct=Liste_dir.copy()
                        if Temps_recolte_passe==Temps_recolte:
                            Temps_recolte_passe=0
                            Arrivée=2
                            Liste_dir=[]
                            for k in Liste_direct:
                                (a,b),(c,d),T_groupe=k
                                Liste_dir.append(((a,b),(x0,y0),T_groupe))
                            Liste_direct=Liste_dir.copy()
                            
                    elif Arrivée==2:
                        Liste_dir=[]
                        for k in Liste_direct:
                            (a,b), (c,d),T_groupe= k
                            if (a,b)!=(c,d):
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
                                    if (a,b,1) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de guêpes (qui n'attaquent pas en hiver)
                                        T_groupe=T_groupe-5
                                        if T_groupe<0:
                                            T_groupe=0
                                    if (a,b,2) in Liste_guepes and saison!='hiver': #le groupe est à la position d'un nid de frelons (qui n'attaquent pas en hiver)
                                        T_groupe=T_groupe-75
                                        if T_groupe<0:
                                            T_groupe=0
                            Liste_dir.append(((a,b),(c,d),T_groupe))
                        Liste_direct=Liste_dir.copy()
                        valid=0 #permet de vérifier si toutes les abeilles sont arrivées à destination
                        for k in Liste_direct:
                            (a,b),(c,d),T_groupe=k
                            if (a,b)==(c,d):
                                valid=valid+1
                        if valid == len(Liste_direct):
                            Arrivée=3
                            Liste_dir=[]
                            for k in Liste_direct:
                                (a,b),(c,d),T_groupe=k
                                Nb_ab_dedans=Nb_ab_dedans+T_groupe
                                qtt_miel=qtt_miel+13*T_groupe #chaque abeille ramène 13 mg de miel
                            if parasitage==1:
                                qtt_miel=qtt_miel-3296 #3kg de miel perdus en été  avec parasitage de lvl 1
                            if parasitage==2:
                                qtt_miel=qtt_miel-6593 #6kg de miel perdus en été  avec parasitage de lvl 2
                            if qtt_miel>30000000: #capacité de miel maximum dans une rûche en mg
                                qtt_miel=30000000
                                essaimage=1
                            if qtt_miel<0:
                                qtt_miel=0
                                Liste_dir.append(((a,b),(c,d),0))
                            but_dehors=0
                            Liste_direct=Liste_dir.copy()
                                    
                elif Arrivée==3:
                    Temps_recolte_passe=Temps_recolte_passe+1
                    if Temps_recolte_passe==Temps_interrecolte:
                        Temps_recolte_passe=0
                        Arrivée=0
            
            """Nb_abeilles_dh=0  """    #vérification en cas de bug de type "nombre d'abeilles négatif)    
            if but_dehors==0:  
                Nb_abeilles=Nb_ab_dedans
            else:
                Nb_abeilles=Nb_ab_dedans
                for k in Liste_direct:
                    _,_,T_groupe=k
                    Nb_abeilles=Nb_abeilles+T_groupe
                """for k in Liste_direct:
                    _,_,T_groupe=k
                    Nb_abeilles_dh=Nb_abeilles_dh+T_groupe
            print(Nb_ab_dedans,Nb_abeilles_dh,Nb_abeilles)"""
            
            """print((x0,y0,Nb_abeilles,Nb_ab_dedans,but_dehors,reperage,liste_reper.copy(),distance,Arrivée,Liste_direct.copy(),Temps_recolte_passe,qtt_miel,parasitage),'\n',s)"""
            #vérification de dernier recours en cas de bug redoutable
            """print(Nb_abeilles,s)""" #vérification rapide en cas de bug majeur
            Info_ruches_copy.append((x0,y0,Nb_abeilles,Nb_ab_dedans,but_dehors,reperage,liste_reper.copy(),distance,
                                     Arrivée,Liste_direct.copy(),Temps_recolte_passe,qtt_miel,parasitage,essaimage,age_reine,esperance_reine))
            Nb_abeilles_tot=Nb_abeilles_tot+Nb_abeilles
        Liste_Nb_abeilles_tot.append(Nb_abeilles_tot)
        Info_ruches=Info_ruches_copy.copy()
    
        
        terrain=np.zeros([N,N])
        for a in range(N):
            for b in range(N):
                    for k in Info_ruches:
                        x0,y0,_,Nb_ab_dedans,_,_,_,_,_,Liste_direct,_,_,_,_,_,_=k
                        if (a,b)==(x0,y0):
                            terrain[a][b]=terrain[a][b]+Nb_ab_dedans
                        for i in Liste_direct:
                            (c,d),_,T_groupe=i
                            if (c,d)==(a,b):
                                terrain[a][b]=terrain[a][b]+T_groupe
                                
        results.append(terrain.copy())
    return(results,Liste_Nb_abeilles_tot)
 
results,Liste_Nb_abeilles_tot=simulation()


"""for i in range(len(results)):
    print(results[i],'\n',i)""" #vérification assez rapide pour détecter de potentiels bugs

fig = plt.figure()
# results[i] contient l'état au pas de temps i sous forme de matrice
im = plt.imshow(results[0], animated=True)
def updatefig(i):
    im.set_array(results[i+1])
    
    return im,
ani = anim.FuncAnimation(fig, updatefig, frames=1000, interval=50, blit=True)
plt.show() #affiche la simulation
