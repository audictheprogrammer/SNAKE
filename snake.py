from upemtk import *
from random import randint
from time import time, sleep

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

lst_color = ['darkgreen', 'green', 'deepskyblue', 'skyblue', 'violet', 'plum', 'orangered', 'tomato']

random_indice = randint(0, 6)

#coordonnées des obstacles
murs = [(10, 3), (10,4), (10, 5), (10, 6),(11, 3), (11,4), (11, 5), (11, 6), (12, 3), (12,4), (12, 5), (12, 6), (13, 3),
    (13,4), (13, 5), (13, 6), (32,8),(32,9),(33,8),(33,9),(34,8),(34,9),(35,8), (35,9), (36,8), (36,9), (37,8),(37, 9), (38,8), (38, 9),
    (30, 25), (30,26), (31, 25), (31,26), (32, 25), (32,26), (33, 25), (33,26), (34, 25), (34,26), (7, 28), (8, 28), 
    (9, 28), (7, 15), (8, 15), (19, 14), (20, 14), (21, 14),(19, 15), (20, 15), (21, 15),(26, 9), (27, 9), (26, 10), (27, 10), (15, 22)]


def case_vers_pixel(case) :
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes) :

    for pomme in pommes :

        x, y = case_vers_pixel(pomme)

        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')

        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')


def affiche_serpent(serpent) :
    '''
    dessine le serpent au coordonnées voulu

    :entree: serpent -> list
    :sortie: aucune
    '''

    for i in range(0, len(serpent)):
        x, y = case_vers_pixel(serpent[i])   

        cercle(x, y, taille_case/2 + 1,
                couleur= choix_color, remplissage= choix_rempl)

def affiche_obstacle(murs) :
    '''
    dessine les obstacles que le serpent doit esquiver tout au long de la partie
    :entree: murs -> list
    '''

    for i in range(0, len(murs)) :
        x, y = case_vers_pixel(murs[i])   

        cercle(x, y, taille_case/2 + 1,
                couleur= 'indigo', remplissage= 'purple')

def change_direction(direction, touche):
    '''
    change la direction que le serpent doit prendre
    le serpent ne peut pas reculer

    :entree: direction -> tuple | touche
    :sortie: direction -> tuple

    >>> change_direction((0, 1), 'Right')
    (1, 0)

    >>> change_direction((1, 0), 'Down')
    (0, 1)
    '''
    if touche == 'Up' and direction != (0, 1) :
        # flèche du haut pressée
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1) :
        # flèche du bas pressée
        return (0, 1)
    elif touche == 'Right' and direction != (-1, 0) :
        # flèche de droite pressée
        return (1, 0)
    elif touche == 'Left' and direction != (1, 0) :
        # flèche de gauche pressée
        return (-1, 0)
    else:
        # aucune touche
        # pas de changement !
        return direction


def ajoute_pommes(pommes, serpent) :
    '''
    ajoute une nouvelle pomme dans la liste pommes
    une pomme ne peut pas apparaitre sur le serpent

    :param pommes: liste des coordonnées des cases contenant des pommes
    :param serpent: coordonnées de la tête du serpent
    :return lst: renvoie la liste avec une nouvelle coordonnées de cases contenant une pommes

    # lorsque nous essayons de mettre un doctest nous obtenons toujours une erreur car
    # les coordonnes des pommes sont aléatoires
    '''
    coordonnes = (randint(0,39), randint(0,29))

    if coordonnes not in serpent and coordonnes not in pommes and coordonnes not in murs:

        pommes.append((coordonnes))

    return pommes

def efface_pommes(pommes, serpent) :
    '''
    enlève la pomme (que le serpent vient de manger) de la liste pommes

    :entree: pommes -> list | serpent -> list
    :sortie: pommes -> 
    
    >>> efface_pommes([(22, 1), (14, 24)], [[22, 1]])
    [(14, 24)]
    '''

    for i in range(0, len(pommes)) :
        
        if serpent[0] == list(pommes[i]) :

            pommes.remove((pommes[i]))

            return pommes

    return pommes

def bouge_serpent(serpent) :

    """
    fonction qui decale tous elements de la liste vers la droite, sauf pour le premier
    exemple:[[12,12],[12,11],[12,10]] -> [[12,13],[12,12],[12,11]]

    :entree: serpent-> list
    :sortie: serpent-> list
    """

    log = list(serpent[0])

    for i in range(len(serpent)) :
        serpent[i], log = log,serpent[i]

    serpent[0][0] += direction[0]
    serpent[0][1] += direction[1]
    
    return list(serpent)

def agrandit_serpent(pommes, serpent):
    '''
    ajoute un élément dans la liste serpent lorsque le serpent passe sur une pommes
    et enlève la pomme mangé de la liste pommes

    :entree: serpent -> list | pommes -> list
    :sortie: serpent -> list
    '''

    for i in range(0, len(pommes)) :

        if serpent[0] == list(pommes[i]) :

            serpent.append(list(pommes[i]))
            efface_pommes(pommes,serpent)

            return list(serpent)

    return list(serpent)

def check_perdu(serpent, murs):
    '''
    vérifie si l'on a perdu
    on perd lorsque l'on sort de la fenêtre, lorsque le serpent se mange, ou lorsque le serpent rentre dans un obstacle

    :entree: serpent -> list
    :sortie: True (si l'on pas encore perdu) | False (si l'on a perdu) et la bouche jouer se finit

    >>> check_perdu([[40, 5]], [[20, 20]])
    False

    >>> check_perdu([[24, 8], [24, 8]], [20, 20])
    False

    >>> check_perdu([[20, 20]], [(20, 20)])
    False

    >>> check_perdu([[20, 20]], [25, 27])
    True
    '''

    #si on sort de la fenetre
    if serpent[0][0] < 0 or serpent[0][0] > 39 or serpent[0][1] < 0 or serpent[0][1] > 29 :

        return False

    #si le serpent se mange
    list_tempo = []
    for i in range(1, len(serpent)) :

        list_tempo.append(serpent[i])

    if serpent[0] in list_tempo :

        return False

    #si le serpent se prend un obstacle
    if tuple(serpent[0]) in murs :

        return False

    return True

# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10    # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)  # direction initiale du serpent
    pommes = [] # liste des coordonnées des cases contenant des pommes
    serpent = [[0, 0]] # liste des coordonnées de cases adjacentes décrivant le serpent
    cree_fenetre(taille_case * largeur_plateau,
                 taille_case * hauteur_plateau)
    
    pause = 35 # pause de X frames entre l'apparition de chaque pommes
    cmpt = 0

    # boucle principale
    jouer = True
    while jouer:
        print(direction)
        if random_indice % 2 == 0 :
            choix_color = lst_color[random_indice]
            choix_rempl = lst_color[random_indice + 1]
        elif random_indice % 2 != 0 :
            choix_color = lst_color[random_indice - 1]
            choix_rempl = lst_color[random_indice]
        elif random_indice == 0 :
            choix_color = lst_color[random_indice]
            choix_rempl = lst_color[random_indice + 1]

        # affichage des objets
        efface_tout()
        if (cmpt > pause or len(pommes) == 0) and direction != (0,0):
            ajoute_pommes(pommes, serpent)
            cmpt = 0
            random_indice = randint(0, 6)

        affiche_obstacle(murs)
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
            direction = change_direction(direction, touche(ev))

        cmpt += 1
        jouer = check_perdu(serpent, murs)

        # attente avant rafraîchissement
        sleep(1/framerate)

    # fermeture et sortie
    ferme_fenetre()

# score final
print("Vous avez mangé", len(serpent)-1, "pommes.")
