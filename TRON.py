import tkinter as tk
import random
import numpy as np
import copy
import time

#################################################################################
#
#   Données de partie

Data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

GInit = np.array(Data, dtype=np.int8)
GInit = np.flip(GInit, 0).transpose()

LARGEUR = 13
HAUTEUR = 17

# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int32)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int32)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int32)

Debug = False
nb = 10000 # nb de parties


# container pour passer efficacement toutes les données de la partie


class Game():
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score = Score
        self.Grille = Grille

    def copy(self):
        return copy.deepcopy(self)

    def move(self, x, y):
        self.PlayerX += x
        self.PlayerY += y


GameInit = Game(GInit, 3, 5)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L


Window = tk.Tk()
Window.geometry(str(largeurPix) + "x" + str(hauteurPix))  # taille de la fenetre
Window.title("TRON")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
PageActive = 0


def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame


def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()


Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0, width=largeurPix, height=hauteurPix, bg="black")
canvas.place(x=0, y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()

    def DrawCase(x, y, coul):
        x *= L
        y *= L
        canvas.create_rectangle(x, H - y, x + L, H - y - L, fill=coul)

    # dessin des murs

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if Game.Grille[x, y] == 1:
                DrawCase(x, y, "gray")
            if Game.Grille[x, y] == 2:
                DrawCase(x, y, "cyan")

    # dessin de la moto
    DrawCase(Game.PlayerX, Game.PlayerY, "red")


def AfficheScore(Game):
    info = "SCORE : {}".format(Game.Score)
    canvas.create_text(80, 13, font="Helvetica 12 bold", fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI


def PlayerPossibleMove(Game):
    x, y = Game.PlayerX, Game.PlayerY
    move = []

    if Game.Grille[x][y - 1] == 0:
        move.append((0, -1))
    if Game.Grille[x][y + 1] == 0:
        move.append((0, 1))
    if Game.Grille[x + 1][y] == 0:
        move.append((1, 0))
    if Game.Grille[x - 1][y] == 0:
        move.append((-1, 0))

    return move

def Simulate(Game):


    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    boucle = True
    if Debug : AffGrilles(G,X,Y)

    # VOTRE CODE ICI
    scoreintsum=0
    while(boucle) :

        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2


        # Direction : 2 = vers le haut

        LPossibles = np.zeros((nb,4),dtype=np.int32)
        Tailles = np.zeros(nb,dtype=np.int32)

        Vgauche = G[I,X-1,Y]
        Vgauche = (Vgauche == 0) * 1

        LPossibles[I,Tailles] = Vgauche
        Tailles += Vgauche

        Vhaut = G[I,X,Y+1]
        Vhaut = (Vhaut == 0) * 1

        LPossibles[I,Tailles] = Vhaut*2
        Tailles += Vhaut

        Vdroite = G[I,X+1,Y]
        Vdroite = (Vdroite == 0) * 1

        LPossibles[I,Tailles] = Vdroite*3
        Tailles += Vdroite

        Vbas = G[I,X,Y-1]
        Vbas = (Vbas == 0) * 1

        LPossibles[I,Tailles] = Vbas*4
        Tailles += Vbas

        Tailles[Tailles==0]=1
        if Debug :print("Taille : ",Tailles)

        R = np.random.randint(Tailles)

        Choix = LPossibles[I,R]
        S[I]+=(Choix[I]!=0)*1

        #DEPLACEMENT
        DX = dx[Choix]
        DY = dy[Choix]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY

        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)
        if np.sum(S)==scoreintsum :
            boucle = False
        else : scoreintsum=np.sum(S)

    return np.mean(S)



"""def Simulation(Game):
    while True:
        possibleMove = PlayerPossibleMove(Game)
        if not possibleMove:
            return Game.Score

        choix = random.randrange(len(possibleMove))

        Game.Grille[Game.PlayerX, Game.PlayerY] = 2

        Game.PlayerX += possibleMove[choix][0]
        Game.PlayerY += possibleMove[choix][1]
        Game.Score += 1"""

def simulategame(Game):
    L=PlayerPossibleMove(Game)
    if len(L) == 0 : return 111
    Listetot=[]
    x=len(L)
    for i in L :
        Game2=Game.copy()
        Game2.PlayerX+=i[0]
        Game2.PlayerY+=i[1]
        Listetot.append(Simulate(Game2))
    t=max(Listetot)
    for y in range(len(Listetot)) :
        if Listetot[y]==t :
            return L[y]


def Play(game):
    x, y = game.PlayerX, game.PlayerY

    game.Grille[x, y] = 2  # laisse la trace de la moto

    possibleMove = simulategame(game)
    if possibleMove!=111:
        game.PlayerX+=possibleMove[0]
        game.PlayerY+=possibleMove[1]
        game.Score += 1
        return False
    else :
        y+=1
        return True


    """if not possibleMove:
        return True

    resultDict = {}
    npPossibleMove = np.array(possibleMove)
    nbPossibleMove = npPossibleMove.shape[0]

    lattice = np.empty( (nbPossibleMove), dtype=object)
    lattice.flat = [game.copy() for _ in lattice.flat]

    for idx, move in enumerate(possibleMove):
        # copy le jeu
        copyGame = game.copy()

        # bouge le personnage
        copyGame.PlayerX = copyGame.PlayerX + move[0]
        copyGame.PlayerY = copyGame.PlayerY + move[1]

        # lance la sumlation
        resultDict[idx] = MonteCarlo(copyGame)

    bestDirection = possibleMove[max(resultDict, key=resultDict.get)]
    game.PlayerX += bestDirection[0]  # valide le déplacement
    game.PlayerY += bestDirection[1]  # valide le déplacement
    game.Score += 1
    return False  # la partie continue
    """

################################################################################

CurrentGame = GameInit.copy()


def Partie():
    Tstart = time.time()
    PartieTermine = Play(CurrentGame)
    #print(time.time() - Tstart)

    if not PartieTermine:
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        Window.after(10, Partie)
    else:
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(10, Partie)
Window.mainloop()
