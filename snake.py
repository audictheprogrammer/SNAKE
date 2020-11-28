from upemtk import *
from random import randint
from time import time, sleep

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):

    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')


def affiche_serpent(serpent):

    for i in range(0, len(serpent)):
        x, y = case_vers_pixel(serpent[i])   

        cercle(x, y, taille_case/2 + 1,
                couleur='darkgreen', remplissage='green')


def change_direction(direction, touche):
    '''
    indique la direction que le serpent doit prendre
    '''
    if touche == 'Up' and direction!=(0,1):
        # flèche du haut pressée
        return (0, -1)
    elif touche == 'Down' and direction!=(0,-1):
        # flèche du bas pressée
        return (0, 1)
    elif touche == 'Right' and direction!=(-1,0) :
        # flèche de droite pressée
        return (1, 0)
    elif touche == 'Left' and direction!=(1,0):
        # flèche de gauche pressée
        return (-1, 0)
    else:
        # aucune touche
        # pas de changement !
        return direction


def ajoute_pommes(pommes, serpent) :
    '''
    ajoute une nouvelle pomme dans la liste pommes
    :param pommes: liste des coordonnées des cases contenant des pommes
    :param serpent: coordonnées de la tête du serpent
    :return lst: renvoie la liste avec une nouvelle coordonnées de cases contenant une pommes
    '''
    coordonnes = (randint(0,39),randint(0,29))

    if coordonnes not in serpent and coordonnes not in pommes :

        pommes.append((coordonnes))

    return pommes

def efface_pommes(pommes, serpent) :

    for i in range(0, len(pommes)) :
        
        if serpent[0] == list(pommes[i]) :

            pommes.remove((pommes[i]))

            return pommes

    return pommes

def bouge_serpent(serpent) :
    log = list(serpent[0])
    for i in range(len(serpent)) :
        serpent[i],log = log,serpent[i]
    serpent[0][0]+=direction[0]
    serpent[0][1]+=direction[1]
    return list(serpent)

def agrandit_serpent(pommes, serpent):

    for i in range(0, len(pommes)) :
        if serpent[0] == list(pommes[i]) :
            serpent.append(list(pommes[i]))
            efface_pommes(pommes,serpent)
            return list(serpent)

    return list(serpent)

# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10    # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    pommes = [] # liste des coordonnées des cases contenant des pommes
    serpent = [[0, 0]] # liste des coordonnées de cases adjacentes décrivant le serpent
    cree_fenetre(taille_case * largeur_plateau,
                 taille_case * hauteur_plateau)
    
    pause = 35 # temps entre chaque apparition de pommes
    cmpt = 0
    score = 0

    ajoute_pommes(pommes, serpent)

    # boucle principale
    jouer = True
    while jouer:

        # affichage des objets
        efface_tout()
        if cmpt > pause or len(pommes) == 0: # temps entre chaque apparition de pommes
            ajoute_pommes(pommes, serpent)
            cmpt = 0
        agrandit_serpent(pommes, serpent)
        bouge_serpent(serpent)
        affiche_pommes(pommes)
        affiche_serpent(serpent)
   
        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            print(touche(ev))
            direction = change_direction(direction, touche(ev))
        cmpt += 1

        #SI ON TRAVERSE LA GAUCHE POUR ARRIVER A DROITE
        #serpent[0][0]%=40
        #serpent[0][1]%=30

        #SI ON RESTE DANS LE CADRE
        """serpent[0][0]=min(39,serpent[0])
        serpent[0][0]=max(0,serpent[0])
        serpent[0][1]=min(39,serpent[1])
        serpent[0][1]=max(0,serpent[1])"""

        # perdu #| si on sort de la fenêtre
        if serpent[0][0] < 0 or serpent[0][0] > 39 or serpent[0][1] < 0 or serpent[0][1] > 29 :
            jouer = False
            print("#########\n# Perdu #\n#########")


        # attente avant rafraîchissement
        sleep(1/framerate)

    # fermeture et sortie
    ferme_fenetre()

print("Vous avez mangé", len(serpent)-1, "pommes.")
