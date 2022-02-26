import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np


##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]


TBL = np.array(TBL,dtype=np.int32)
TBL = TBL.transpose()  ## ainsi, on peut écrire TBL[x][y]

DIST = [[999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999],
        [999,100,100,100,100,999,100,100,100,100,100,100,100,100,999,100,100,100,100,999],
        [999,100,999,999,100,999,100,999,999,999,999,999,999,100,999,100,999,999,100,999],
        [999,100,999,100,100,100,100,100,100,100,100,100,100,100,100,100,100,999,100,999],
        [999,100,999,100,999,999,100,999,999,998,998,999,999,100,999,999,100,999,100,999],
        [999,100,100,100,100,100,100,999,998,998,998,998,999,100,100,100,100,100,100,999],
        [999,100,999,100,999,999,100,999,999,999,999,999,999,100,999,999,100,999,100,999],
        [999,100,999,100,100,100,100,100,100,100,100,100,100,100,100,100,100,999,100,999],
        [999,100,999,999,100,999,100,999,999,999,999,999,999,100,999,100,999,999,100,999],
        [999,100,100,100,100,999,100,100,100,100,100,100,100,100,999,100,100,100,100,999],
        [999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999] ]

DIST = np.array(DIST,dtype=np.int32)
DIST = DIST.transpose()

PacManPos = [5,5]




HAUTEUR = TBL.shape [1]
LARGEUR = TBL.shape [0]
SCORE = 0
MODE = "fuite"
tour = 0
gameover = False
win = False

def PlacementsGUM():
   GUM = np.zeros(TBL.shape)

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
            DIST[x][y] = 0
         if ( TBL[x][y] == 3):
            GUM[x][y] = 2
            DIST[x][y] = 0
   return GUM

GUM = PlacementsGUM()

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink",     (0,0) ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange",   (0,0) ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan",     (0,0) ])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red",      (0,0) ])

##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

# création de la fenetre principale  -- NE PAS TOUCHER


ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' :
      PAUSE_FLAG = not PAUSE_FLAG

Window.bind("<KeyPress>", keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
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


def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')

def distanceMapGhost():
   global mapAvoidGhosts
   mapAvoidGhosts = np.zeros(TBL.shape)
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (TBL[x][y] == 1):
            mapAvoidGhosts[x][y] = 999
         if (TBL[x][y] in [0,2,3]):
            mapAvoidGhosts[x][y] = 100
   for Ghost in Ghosts:
      mapAvoidGhosts[Ghost[0]][Ghost[1]] = 0

   a = True
   while a:
      a = False
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if(mapAvoidGhosts[x][y] == 999 or mapAvoidGhosts[x][y] == 0): continue
            values = [mapAvoidGhosts[x-1][y],mapAvoidGhosts[x+1][y], mapAvoidGhosts[x][y-1], mapAvoidGhosts[x][y+1]]
            if(min(values) >= 100): continue
            if(mapAvoidGhosts[x][y] > min(values)+1):
               mapAvoidGhosts[x][y] = min(values)+1
               a = True
            elif(mapAvoidGhosts[x][y] == min(values)):
               mapAvoidGhosts[x][y] += 1
               a = True
            elif(mapAvoidGhosts[x][y] < min(values)):
               mapAvoidGhosts[x][y] = min(values)+1
               a = True

distanceMapGhost()

def To(coord):
   return coord * ZOOM + ZOOM

# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche():
   global anim_bouche, DIST, gameover

   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)

   canvas.delete("all")


   # murs

   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x)
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")

   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y)
         if ( GUM[x][y] == 1):
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
         if ( GUM[x][y] == 2):
            e = 9
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="purple")

   # dessine pacman
   xx = To(PacManPos[0])
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche]
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = "yellow")
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche


   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0])
      yy = To(P[1])
      e = 16
      if MODE == "chasse" :
         coul = "blue"
      else :
         coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)

      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")

      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")

      dec += 3

   # texte
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text ="score: {}".format(SCORE), fill ="yellow", font = PoliceTexte)

   #distance pacman/pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y)
         e = 15
         if DIST[x][y] != 999 :
            canvas.create_text(xx-e,yy-e, text = int(DIST[x][y]), fill ="white", font=(PoliceTexte, 6))

   #distance pacman/ghost
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x)
         yy = To(y)
         e = 15
         if DIST[x][y] != 999 :
            canvas.create_text(xx,yy-e, text = int(mapAvoidGhosts[x][y]), fill ="red", font=(PoliceTexte, 6))

   if(gameover == True):
      canvas.create_text(screeenWidth // 2, screenHeight // 2 , text = "GAME OVER", fill ="yellow", font=(PoliceTexte,30))
   if(win == True) :
      canvas.create_text(screeenWidth // 2, screenHeight // 2 , text = "PACMAN WINS !", fill ="yellow", font=(PoliceTexte,30))

#########################################################################

#  Partie III :   Gestion de partie   -   placez votre code dans cette section

#########################################################################

def PacManPossibleMove(mode):
   global tour
   direction = ""
   x,y = PacManPos
   if(mode == "chasse"):
      nearF = {
         "TOP": mapAvoidGhosts[x][y-1],
         "BOT": mapAvoidGhosts[x][y+1],
         "LEFT": mapAvoidGhosts[x-1][y],
         "RIGHT": mapAvoidGhosts[x+1][y]
      }
      nearF = {i:nearF[i] for i in nearF if nearF[i]!=999}
      direction = min(nearF, key=nearF.get)
      tour +=1
   else:
      if(mapAvoidGhosts[x][y] <= 3):
         nearF = {
            "TOP": mapAvoidGhosts[x][y-1],
            "BOT": mapAvoidGhosts[x][y+1],
            "LEFT": mapAvoidGhosts[x-1][y],
            "RIGHT": mapAvoidGhosts[x+1][y]
         }
         nearF = {i:nearF[i] for i in nearF if nearF[i]!=999}
         direction = max(nearF, key=nearF.get)
      else:
         Path = {
            "TOP": DIST[x][y-1],
            "BOT": DIST[x][y+1],
            "LEFT": DIST[x-1][y],
            "RIGHT": DIST[x+1][y]
         }
         direction = min(Path, key=Path.get)

   if(direction == "TOP"): return [0,-1]
   if(direction == "BOT"): return [0,1]
   if(direction == "LEFT"): return [-1,0]
   if(direction == "RIGHT"): return [1,0]

   return [0,0]

def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L

def distanceMap():
   bool = True
   while bool:
      bool = False
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if(DIST[x][y] == 999 or DIST[x][y] == 0): continue
            values = [DIST[x-1][y],DIST[x+1][y], DIST[x][y-1], DIST[x][y+1]]
            if(DIST[x][y] > min(values)+1):
               DIST[x][y] = min(values)+1
               bool = True
            elif(DIST[x][y] == min(values)):
               DIST[x][y] += 1
               bool = True
            elif(DIST[x][y] < min(values)):
               DIST[x][y] = min(values)+1
               bool = True

def CheckCollision():
   global PacManPos, Ghosts, MODE, SCORE, gameover
   #print(MODE)
   for Ghost in Ghosts:
      #print("Pacman : " + str(PacManPos[0]) + " , " + str(PacManPos[1]) + " | Fantome : " +str(Ghost[2]) +" , "+ str(Ghost[0]) + " , "+str(Ghost[1]))
      if(PacManPos[0] == Ghost[0] and PacManPos[1] == Ghost[1]):
         if(MODE == "chasse"):
            Ghost[0] = LARGEUR // 2
            Ghost[1] = HAUTEUR // 2
            SCORE += 2000
         else :
            gameover = True

def checkWin() :
   global win, DIST

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if DIST[x][y] == 1000 :
            win = True


def IA():
   global PacManPos, Ghosts, SCORE, MODE, tour

   if(tour >= 16):
      MODE = "fuite"
      tour = 0


   #deplacement Pacman
   L = np.add(PacManPos, PacManPossibleMove(MODE))
   if(TBL[L[0]][L[1]] in [0,3]):
      PacManPos = L

   if(GUM[PacManPos[0]][PacManPos[1]] == 1):
      SCORE+= 100
   elif(GUM[PacManPos[0]][PacManPos[1]] == 2):
      SCORE+= 100
      MODE = "chasse"

   if(GUM[PacManPos[0]][PacManPos[1]] in [1,2]):
      GUM[PacManPos[0]][PacManPos[1]] = 0
      DIST[PacManPos[0]][PacManPos[1]] = 100

   #vérification de collision entre fantôme et pacman
   CheckCollision()

   #deplacement Fantome
   for F in Ghosts:
      if(TBL[F[0]][F[1]] == 2):
         F[1] -= 1
         F[3] = (0,-1)
         continue

      L = GhostsPossibleMove(F[0],F[1])
      if(len(L) == 2 and F[3] in L):
         F[0] += F[3][0]
         F[1] += F[3][1]
         continue

      rand = random.random()

      if(F[2] == 'pink' and (0,1) in L and rand >= 0.8):
         F[1] += 1
         F[3] = (0,1)
         continue
      if(F[2] == 'orange' and (0,-1) in L and rand >= 0.8):
         F[1] -= 1
         F[3] = (0,-1)
         continue
      if(F[2] == 'cyan' and (1,0) in L and rand >= 0.8):
         F[0] += 1
         F[3] = (1,0)
         continue
      if(F[2] == 'red' and (-1,0) in L and rand >= 0.8):
         F[0] -= 1
         F[3] = (-1,0)
         continue

      choixFantome = random.randrange(len(L))
      F[0] += L[choixFantome][0]
      F[1] += L[choixFantome][1]
      F[3] = L[choixFantome]

   #vérification de collision entre fantôme et pacman
   CheckCollision()

   #prise des pac-gommes
   if GUM[PacManPos[0]][PacManPos[1]] == 1 :
      SCORE += 1
      GUM[PacManPos[0]][PacManPos[1]] = 0
      DIST[PacManPos[0]][PacManPos[1]] = 100


   #mise a jour des matrices de distance
   distanceMap()
   distanceMapGhost()

   #verification si la partie est gagnée

   checkWin()

#  Boucle principale de votre jeu appelée toutes les 500ms

def MainLoop():
   if(gameover == False and win == False):
      IA()
      #print(DIST)
      Affiche()

###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()
