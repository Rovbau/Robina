#!/usr/bin/env python3

from math import cos,sin,radians,asin,degrees
from tkinter import *
import pickle
import time
#Kartennull für TK
Nullx=200
Nully=380

#Tkinter 
root=Tk()
root.title ("Hinderniss-Daten")           #Titel de Fensters
root.geometry("700x700+0+0")
can=Canvas(master=root, width=600, height=600, bg="grey")
#Karten Nullpunkt



def printObstacles():
    try:
        can.delete("Point")
        obstacles_in_grid = pickle.load( open("RoboObstacles.p" , "rb" ))
        for pos in obstacles_in_grid:
            X=pos[0]*10
            Y=pos[1]*10
            #Zeichne Hindernisspunkte Global ein 
            can.create_rectangle(Nullx+X-5,Nully-Y+5,Nullx+X+5,Nully-Y-5, width=1, fill="red",tag="Point")

        position_in_grid = pickle.load( open("RoboPath.p" , "rb" ))

        for pos in position_in_grid:
            X=pos[0]
            Y=pos[1]
            #Zeichne Hindernisspunkte Global ein 
            can.create_oval(Nullx+X-15,Nully-Y+15,Nullx+X+15,Nully-Y-15, width=1, fill=None,tag="Point")

        position_solved_path = pickle.load( open("RoboSolved.p" , "rb" ))

        for pos in position_solved_path:
            X=pos[0]*10
            Y=pos[1]*10
            #Zeichne Hindernisspunkte Global ein 
            can.create_oval(Nullx+X-3,Nully-Y+3,Nullx+X+3,Nully-Y-3, width=1, fill="green",tag="Point")
            
        print(time.time())   
        root.after(1500,printObstacles)
    except:
        print("ERROR")
        time.sleep(0.5)
        printObstacles()


###MAIN###
printObstacles()
can.create_oval(Nullx-2,Nully+2,Nullx+2,Nully-2, width=1, fill="black")
can.create_oval(Nullx-50,Nully+50,Nullx+50,Nully-50, width=1, fill=None)
can.create_oval(Nullx-100,Nully+100,Nullx+100,Nully-100, width=1, fill=None)
can.create_oval(Nullx-150,Nully+150,Nullx+150,Nully-150, width=1, fill=None)
can.pack()
root.mainloop()
