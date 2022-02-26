import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import time

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 500
HAUT = 500

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

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
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
           
winner = "blue" 
score = 0
score2 = 0
###############################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 
def win(qui):
    if(Grille[2][0] == qui and Grille[0][2] == qui and Grille[1][1]==qui):#diagonale haut-bas
         
        return True
    elif(Grille[0][0] == qui and Grille[1][1] == qui and Grille[2][2]==qui):#diagonale bas-haut
         
        return True
    elif(Grille[0][2] == qui and Grille[1][2] == qui and Grille[2][2]==qui):#ligne Grille[x][2]
         
        return True
    elif(Grille[0][1] == qui and Grille[1][1] == qui and Grille[2][1]==qui):#ligne Grille[x][1]
         
        return True
    elif(Grille[0][0] == qui and Grille[1][0] == qui and Grille[2][0]==qui):#ligne Grille[x][0]
         
        return True
    elif(Grille[2][0] == qui and Grille[2][1] == qui and Grille[2][2]==qui):#ligne Grille[2][x]
         
        return True
    elif(Grille[1][0] == qui and Grille[1][1] == qui and Grille[1][2]==qui):#ligne Grille[1][x]
         
        return True
    elif(Grille[0][0] == qui and Grille[0][1] == qui and Grille[0][2]==qui):#ligne Grille[0][x]

        return True
    else:
        return False
def Play(x,y):  
        
        Equal()    
        HumainWIN()
        IAWIN()
    
        
def HumainWIN():
    global winner, score
    if win(1) : 
        score += 1
        winner = "red"
        Dessine()
        PartieGagnee = True
        for x in range(3):
            for y in range(3):
                Grille[x][y] = 0
       
    
def IAWIN():
    global winner, score2
    
    
    
    if win(2) :
        score2 += 1
        winner = "yellow"
        Dessine()
        time.sleep(0.2)
        PartieGagnee = True
        for x in range(3):
            for y in range(3):
                Grille[x][y] = 0

def Equal():
    global winner
    if nonFull() == False :
        winner = "white"
        Dessine()
        time.sleep(0.2)
        DebutDePartie =  True
        for x in range(3):
            for y in range(3):
                Grille[x][y] = 0
        return
        
def JoueurSimuleIA(Gri):
    L = nonFullMemo()
    if win(2) or win(1) :
        return (1,0)
    if nonFull()== False:
        return (0,0)
    
    result=[]
    for coup in L :
        Grille[coup[0]][coup[1]] = 2
        R = JoueurSimuleHumain(Gri) #Rentabilité du coup
        result.append(R[0]) 
        Grille[coup[0]][coup[1]] = 0
        min_value = None
        min_idx = None
        for idx, num in enumerate(result):
            if (min_value is None or num < min_value): #Quel coup est le plus rentable
                min_value = num
                min_idx = idx #quel est la position du coup rentable dans le tableau de disponible

        minI = (min_value,min_idx) #le coup le plus rentable et sa position 
    return minI

        
    
def JoueurSimuleHumain(Gri):
    L = nonFullMemo()
    if win(2) or win(1) :
        return (-1,0)
    if nonFull()== False:
        return (0,0)
    result=[]
    for coup in L :
        Grille[coup[0]][coup[1]] = 1
        R = JoueurSimuleIA(Gri) #Rentabilité du coup
        result.append(R[0])
        Grille[coup[0]][coup[1]] = 0
        
        max_value = None
        max_idx = None
        
        for idx, num in enumerate(result):#Quel coup est le plus rentable
            if (max_value is None or num > max_value):
                max_value = num
                max_idx = idx#quel est la position du coup rentable dans le tableau de disponible

        MaxI = (max_value,max_idx)

    return MaxI


    
    
################################################################################
#    
# Dessine la grille de jeu

def Dessine(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
       
        global winner

        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill=winner, width="4" )
            canvas.create_line(0,i*100,300,i*100,fill=winner, width="4" ) 
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
        msg = 'score : ' + str(score) + " - " + str(score2)
        canvas.create_text(150,340, font=('Helvetica', 24), text = msg, fill="grey")
        canvas.update()   
        if score ==  score2 :
            canvas.create_text(150,400, font=('Helvetica', 24), text = 'égalité', fill="grey")
            canvas.update() 
        if score < score2 :
            canvas.create_text(200,400, font=('Helvetica', 24), text = "IA prend de l'avance", fill="grey")
            canvas.update() 
        if score > score2 :
            canvas.create_text(200,400, font=('Helvetica', 24), text = "tu prends de l'avance", fill="grey")
            canvas.update() 
        canvas.update()            


def nonFull():
    for x in range(3):
        for y in range(3):
            if(Grille[x][y] == 0 ):
                return True
    return False
def nonFullMemo():
    L = []
    for x in range(3):
        for y in range(3):
            if (Grille[x][y] == 0) : 
                L.append((x,y))
    return L
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin
DebutDePartie =  True
FinDePartie = False
def MouseClick(event):
   
    global DebutDePartie,FinDePartie,winner
    if DebutDePartie :
        for x in range(3):
            for y in range(3):
                Grille[x][y] = 0
        Dessine()
        DebutDePartie = False
    Window.focus_set()
    x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
    y = event.y // 100
    if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
    if (Grille[x][y] != 0) : return

    Grille[x][y] = 1  # gestion du joueur humain et de l'IA
    Dessine()
    
    if FinDePartie :
        DebutDePartie =  True
        canvas.create_text(150,150, font=('Helvetica', 24), text = "END", fill="cyan")  
    else :

        if nonFull() == False :
            winner = "white"
            Dessine()
            time.sleep(0.2)
            DebutDePartie =  True
            for x in range(3):
                for y in range(3):
                    Grille[x][y] = 0
        else :
            Full = nonFullMemo()
            print(JoueurSimuleIA(Grille))
            print(Full)
            Grille[Full[JoueurSimuleIA(Grille)[1]][0]][Full[JoueurSimuleIA(Grille)[1]][1]] = 2 
            Play(x,y)
        if FinDePartie :
            DebutDePartie =  True
            canvas.create_text(150,150, font=('Helvetica', 24), text = "END", fill="cyan") 
    
    Play(x,y)
    Dessine()
    
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine()
Window.mainloop()