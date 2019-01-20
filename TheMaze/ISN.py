from tkinter import *
from random import randint

a = randint(13, 14)

fenetre = Tk()

w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()
img = PhotoImage(file='themaze.png')                                       #on importe le skin du jeu
img2 = PhotoImage(file='fin2.png')

can = Canvas(fenetre, height=700, width=800, background='black')
can.create_image(0, 0, image=img, anchor='nw')              #on définit le canvas et on set les images pour faire le jeu
can.create_image(0, 150, image=img2, anchor='nw')

player = can.create_rectangle(213, 228, 237, 253, outline='blue', fill='blue')  #on crée le player

baseCoords = (213, 228, 237, 253)
PCoords = [213, 228, 237, 253]                  #on définit les coordonnées de base pour plus tard

lvl1 = ['d', 'd', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'd', 'l', 'd', 'l', 'u', 'l', 'd', 'd', 'd', 'd', 'l', 'l',
        'l', 'd', 'd', 'r', 'u''r', 'd', 'r', 'u', 'r', 'u', 'r', 'd', 'd', 'l', 'd']
                            #les niveaux
lvl0 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r']
win = False
path = []
currentlvl = lvl0


def reset():
    print("PANIC")
    path[:] = []
    PCoords[0] = 213
    PCoords[1] = 228
    PCoords[2] = 237
    PCoords[3] = 253    
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    pass


def check():
    if len(path) == 0:
        return [None]   #on check par rapport au maze choisi
    i = len(path) - 1
    if path[i] != currentlvl[i]:
        can.itemconfig(player, outline = 'red', fill = 'red')
    	


def movedown(event):                        # les 4 fonctions de mouvements qui sont quasiment les mêmes
    PCoords[1] = PCoords[1] + 50
    PCoords[3] = PCoords[3] + 50
    path.append('d')

    if PCoords[1] > baseCoords[1] + 400 or PCoords[3] > baseCoords[3] + 399:
        PCoords[1] = PCoords[1] - 50
        PCoords[3] = PCoords[3] - 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path)
    check()


def moveup(event):
    PCoords[1] = PCoords[1] - 50
    PCoords[3] = PCoords[3] - 50
    path.append('u')

    if PCoords[1] < baseCoords[1] or PCoords[3] < baseCoords[3]:
        PCoords[1] = PCoords[1] + 50
        PCoords[3] = PCoords[3] + 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path)
    check()


def moveleft(event):
    PCoords[0] = PCoords[0] - 50
    PCoords[2] = PCoords[2] - 50
    path.append('l')

    if PCoords[0] < baseCoords[0] or PCoords[2] < baseCoords[2]:
        PCoords[0] = PCoords[0] + 50
        PCoords[2] = PCoords[2] + 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path)
    check()


def moveright(event):
    PCoords[0] = PCoords[0] + 50
    PCoords[2] = PCoords[2] + 50
    path.append('r')

    if PCoords[0] > baseCoords[0] + 400 or PCoords[2] > baseCoords[2] + 399:
        PCoords[0] = PCoords[0] - 50
        PCoords[2] = PCoords[2] - 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path)
    check()


def blink():
    current = can.itemcget(player, "state")                     #le perso clignote wouhou
    next = 'hidden' if current == 'normal' else 'normal'
    can.itemconfig(player, state=next)
    fenetre.after(500, blink)


print(path)

can.pack()
fenetre.bind('<Up>', moveup)
fenetre.bind('<Down>', movedown)
fenetre.bind('<Left>', moveleft)
fenetre.bind('<Right>', moveright)
fenetre.focus_set()
blink()
fenetre.mainloop()
