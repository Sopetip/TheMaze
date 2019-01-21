from tkinter import *
from random import randint
import tkinter.font as tkFont

a = randint(13, 14)

fenetre = Tk()

font = tkFont.Font(family="Segoe UI", size=14)

w, h = fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()
img = PhotoImage(file='themaze.png')  # on importe le skin du jeu
img2 = PhotoImage(file='fin2.png')

can = Canvas(fenetre, height=700, width=800, background='black')
can.create_image(0, 0, image=img, anchor='nw')  # on définit le canvas et on set les images pour faire le jeu
can.create_image(0, 150, image=img2, anchor='nw')

player = can.create_rectangle(213, 228, 237, 253, outline='blue', fill='blue')  # on crée le player
clock = can.create_text(113, 558, fill='red', font=font)

baseCoords = (213, 228, 237, 253)
PCoords = [213, 228, 237, 253]  # on définit les coordonnées de base pour plus tard
print(PCoords)

lvl1 = ['d', 'd', 'r', 'u', 'u', 'r', 'r', 'r', 'r', 'r', 'd', 'l', 'd', 'l', 'u', 'l', 'd', 'd', 'd', 'd', 'l', 'l',
        'l', 'd', 'd', 'r', 'u' ,'r', 'd', 'r', 'u', 'r', 'u', 'r', 'd', 'd', 'l']
# les niveaux
lvl0 = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'r', 'r', 'r', 'r']
win = False
path = []
currentlvl = lvl1
error = False

minut = 0
sec = 0
ms = 000

trash = []


def timer():
    global minut
    global sec
    global ms
    global trash
    if len(path) >= 1:

        if ms > 100:
            sec = sec + 1
            ms = 0
        if sec > 60:
            minut = minut + 1
            sec = 0
        if minut > 60:
            minut = 0   
        output = str(minut) + ':' + str(sec) + '.' + str(ms)
        can.itemconfig(clock, text=output)
        ms = ms + 1
    else:
        ms, sec, minut = 0, 0, 0
    if win:
        can.itemconfig(clock, fill ='green')
        return [None]
    if error:
        return [None]
    fenetre.after(10, timer)


def reset():
    print("PANIC")
    path[:] = []
    can.itemconfig(player, outline='blue', fill='blue')
    timer()


def check():  # on check par rapport au maze choisi
    global error
    global win
    if len(path) == 0:
        return [None]

    if error:
        global PCoords
        if PCoords == [213, 228, 237, 253]:
            error = False
            reset()
        return [None]

    i = len(path) - 1

    if path[i] != currentlvl[i]:
        can.itemconfig(player, outline='red', fill='red')
        error = True
    if len(path) == len(currentlvl) and not error:
        win = True
        print("GG")



def movedown(event):  # les 4 fonctions de mouvements qui sont quasiment les mêmes
    PCoords[1] = PCoords[1] + 50
    PCoords[3] = PCoords[3] + 50
    path.append('d')
    trash = event

    if PCoords[1] > baseCoords[1] + 400 or PCoords[3] > baseCoords[3] + 399:
        PCoords[1] = PCoords[1] - 50
        PCoords[3] = PCoords[3] - 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path, PCoords, baseCoords)
    check()


def moveup(event):
    PCoords[1] = PCoords[1] - 50
    PCoords[3] = PCoords[3] - 50
    path.append('u')
    trash = event

    if PCoords[1] < baseCoords[1] or PCoords[3] < baseCoords[3]:
        PCoords[1] = PCoords[1] + 50
        PCoords[3] = PCoords[3] + 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path, PCoords, baseCoords)
    check()


def moveleft(event):
    PCoords[0] = PCoords[0] - 50
    PCoords[2] = PCoords[2] - 50
    path.append('l')
    trash = event

    if PCoords[0] < baseCoords[0] or PCoords[2] < baseCoords[2]:
        PCoords[0] = PCoords[0] + 50
        PCoords[2] = PCoords[2] + 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path, PCoords, baseCoords)
    check()


def moveright(event):
    PCoords[0] = PCoords[0] + 50
    PCoords[2] = PCoords[2] + 50
    path.append('r')
    trash = event

    if PCoords[0] > baseCoords[0] + 400 or PCoords[2] > baseCoords[2] + 399:
        PCoords[0] = PCoords[0] - 50
        PCoords[2] = PCoords[2] - 50
        del path[-1]
    can.coords(player, PCoords[0], PCoords[1], PCoords[2], PCoords[3])
    print(path, PCoords, baseCoords)
    check()


def blink():
    current = can.itemcget(player, "state")  # le perso clignote wouhou
    after = 'hidden' if current == 'normal' else 'normal'
    can.itemconfig(player, state=after)
    fenetre.after(250, blink)


print(path)

can.pack()
fenetre.bind('<Up>', moveup)
fenetre.bind('<Down>', movedown)
fenetre.bind('<Left>', moveleft)
fenetre.bind('<Right>', moveright)
fenetre.focus_set()
timer()
blink()
fenetre.mainloop()
