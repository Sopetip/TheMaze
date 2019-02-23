# coding: utf-8
from tkinter import *
import tkinter.font as tkfont

import winsound

root = Tk()  # on définit la main fenêtre

root.wm_title("The Maze")  # makes the title top left

font = tkfont.Font(family="Segoe UI", size=14)  # on crée une font

winsound.PlaySound('resources/audio/SlamTheTargets.wav', winsound.SND_LOOP | winsound.SND_ASYNC)  # on import le sound du jeu

img = PhotoImage(file='resources/main/themaze.png')  # on importe le skin du jeu
img2 = PhotoImage(file='resources/main/fin2.png')
# lvl1check1 = PhotoImage(file='lvl1check1.png')


can = Canvas(root, height=700, width=800, background='black')

can.create_image(0, 0, image=img, anchor='nw')  # on définit le canvas et on set les images pour faire le jeu
can.create_image(0, 150, image=img2, anchor='nw')

player = can.create_rectangle(213, 228, 237, 253, outline='blue', fill='blue')  # on crée le player
clock = can.create_text(113, 558, fill='red', font=font)  # on set la clock aussi

baseCoords = (213, 228, 237, 253)  # C'est un tuple, genre de liste invariable contrairement à PCoords en dessous.
PCoords = [213, 228, 237, 253]  # on définit les coordonnées de base et du player pour plus tard

lvl1 = ['d', 'd', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'd', 'l', 'd', 'l', 'u', 'l', 'd', 'd', 'd', 'd', 'l', 'l',
        'l', 'd', 'd', 'r', 'u', 'r', 'd', 'r', 'u', 'r', 'u', 'r', 'd', 'd', 'l']
wrlvl1 = [0, 4, 72]  # le world record, pour l'instant détenu par Hélie Lévy. HAHA

lvl2 = ['d', 'r', 'd', 'd', 'r', 'u', 'r', 'd', 'r', 'u', 'u', 'r', 'r', 'd', 'r', 'd', 'd', 'd', 'd', 'd', 'l', 'u',
        'l', 'd', 'l']

lvl3 = ['d', 'r', 'r', 'd', 'l', 'd', 'd', 'r', 'd', 'r', 'r', 'u', 'r', 'd', 'd', 'l', 'd']

# les niveaux
lvl0 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r']
win = False
path = []
currentlvl = lvl1
error = False  # on définit des variables globales pour plus tard.
minut = 0
sec = 0
ms = 000
index = 0
trash = []
levelon = True


def timer():  # on fait le timer.
    global minut
    global sec
    global ms
    if len(path) >= 1:

        if ms > 100:
            sec = sec + 1
            ms = 0
        if sec > 60:
            minut = minut + 1
            sec = 0
        if minut > 60:
            minut = 0
        output = str(minut) + ':' + str(sec) + '.' + str("%.1f" % ms)
        can.itemconfig(clock, text=output)
        ms = ms + 0.1
    else:
        ms, sec, minut = 0, 0, 0
    if win:
        can.itemconfig(clock, fill='green')
        if wrlvl1[1] >= sec:
            if wrlvl1[1] == sec and wrlvl1[2] <= ms:
                pass
            else:
                can.itemconfig(clock, fill='yellow')
        return [None]
    if error:
        return [None]
    root.after(1, timer)


def reset():  # on reset la taille du path, on relance le timer et on remet le personnage de façon normale
    path[:] = []  # selectionner tous les objets de la liste et les remplacer par la liste suivante: rien
    can.itemconfig(player, outline='blue', fill='blue')
    can.itemconfig(clock, fill='red')
    timer()


def check():  # on check si le dernier move du joueur correspond au move demandé par le niveau
    global error
    global win
    global PCoords
    if len(path) == 0:
        return [None]

    if error:
        if PCoords == [213, 228, 237, 253]:
            error = False
            reset()
        return [None]

    if win:
        if PCoords == [213, 228, 237, 253]:
            win = False
            reset()
        return [None]

    i = len(path) - 1

    if path[i] != currentlvl[i]:
        can.itemconfig(player, outline='red', fill='red')
        error = True
    if len(path) == len(currentlvl) and not error:
        win = True
        print("GG")
    print(path)


def blink():
    current = can.itemcget(player, "state")  # le perso clignote wouhou
    after = 'hidden' if current == 'normal' else 'normal'
    can.itemconfig(player, state=after)
    if not levelon:
        return [None]
    root.after(125, blink)


def movedown(event):  # les 4 fonctions de mouvements qui sont quasiment les mêmes.
    global trash  # juste on bouge les coordonnées du player de 50 sur X ou Y
    PCoords[1] = PCoords[1] + 50
    PCoords[3] = PCoords[3] + 50
    path.append('d') #ensuite on append à la fin de la liste 'path' le dernier mouvement exécuté.
    trash = event

    if PCoords[1] > baseCoords[1] + 400 or PCoords[3] > baseCoords[3] + 399: #on vérifie que le joueur n'a pas atteint les limites
        PCoords[1] = PCoords[1] - 50
        PCoords[3] = PCoords[3] - 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == ('u'):
            del path[-1]
            del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    check() #on check que le dernier n'est pas mauvais.


def moveup(event):
    global trash
    PCoords[1] = PCoords[1] - 50
    PCoords[3] = PCoords[3] - 50
    path.append('u')
    trash = event

    if PCoords[1] < baseCoords[1] or PCoords[3] < baseCoords[3]:
        PCoords[1] = PCoords[1] + 50
        PCoords[3] = PCoords[3] + 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == ('d'):
            del path[-1]
            del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    check()


def moveleft(event):
    global trash
    PCoords[0] = PCoords[0] - 50
    PCoords[2] = PCoords[2] - 50
    path.append('l')
    trash = event

    if PCoords[0] < baseCoords[0] or PCoords[2] < baseCoords[2]:
        PCoords[0] = PCoords[0] + 50
        PCoords[2] = PCoords[2] + 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == ('r'):
            del path[-1]
            del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    check()


def moveright(event):
    global trash
    PCoords[0] = PCoords[0] + 50
    PCoords[2] = PCoords[2] + 50
    path.append('r')
    trash = event

    if PCoords[0] > baseCoords[0] + 400 or PCoords[2] > baseCoords[2] + 399:
        PCoords[0] = PCoords[0] - 50
        PCoords[2] = PCoords[2] - 50
        del path[-1]
    if len(path) > 1:
        if path[-2] == ('l'):
            del path[-1]
            del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    check()


def clear(event):
    global trash
    trash = event
    for child in root.winfo_children():
        child.destroy()


can.pack()
root.bind('r', clear)
root.bind('<Up>', moveup)
root.bind('<Down>', movedown)
root.bind('<Left>', moveleft)
root.bind('<Right>', moveright)
root.focus_set()
timer()
blink()
root.mainloop()
print(wrlvl1)
