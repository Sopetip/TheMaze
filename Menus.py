# coding utf-8
from tkinter import *
import tkinter.font as tkfont
import os

menus = Tk()

font = tkfont.Font(family="Segoe UI", size=24)  # on crée une font

menus.wm_title("The Maze")  # makes the title top left
topFrame = Frame(menus, height=300, width=800, bg='black')
topFrame.grid(row=0, column=0, sticky=N)
topFrame.grid_propagate(0)

title = Label(topFrame, text="THE MAZE", font=font, bg="black", fg="white")
title.grid(row=0, column=0)
title.grid_rowconfigure(0, weight=1)
title.grid_columnconfigure(0, weight=1)

leftFrame = Frame(menus, bg='blue', height=400, width=400)
leftFrame.grid(row=1, column=0, sticky=W)
leftFrame.grid_propagate(0)

arcade = Label(leftFrame, text="ARCADE", font=font, bg="black", fg="white")
arcade.grid(row=0, column=0)
arcade.grid_rowconfigure(0, weight=1)
arcade.grid_columnconfigure(0, weight=1)

rightFrame = Frame(menus, bg='red', height=400, width=400)
rightFrame.grid(row=1, column=0, sticky=E)
rightFrame.grid_propagate(0)

history = Label(rightFrame, text="HISTORY", font=font, bg="black", fg="white")
history.grid(row=0, column=0)
history.grid_rowconfigure(0, weight=1)
history.grid_columnconfigure(0, weight=1)


def test(event):
    os.system("ISN.py")


menus.bind('r', test)
menus.mainloop()
