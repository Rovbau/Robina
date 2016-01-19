from math import cos,sin,radians,asin,degrees
from tkinter import *
import pickle
import time
#Kartennull für TK
Nullx=250
Nully=250

#Tkinter 
root=Tk()
root.title ("Hinderniss-Daten")           #Titel de Fensters
#root.geometry("320x240+0+0")
can=Canvas(master=root, width=500, height=580, bg="grey")
#Karten Nullpunkt
can.create_oval(Nullx-5,Nully-5,Nullx,Nully, width=1, fill="black")


def printObstacles():
    obstacles_in_grid = pickle.load( open("RoboObstacles.p" , "rb" ))
    for pos in obstacles_in_grid:
        X=pos[0]*10
        Y=pos[1]*10
        #Zeichne Hindernisspunkte Global ein 
        can.create_oval(Nullx+X-5,Nully-Y-5,Nullx+X,Nully-Y, width=1, fill="red")

    position_in_grid = pickle.load( open("RoboPath.p" , "rb" ))
    for pos in position_in_grid:
        X=pos[0]
        Y=pos[1]
        #Zeichne Hindernisspunkte Global ein 
        can.create_oval(Nullx+X-7,Nully-Y-7,Nullx+X,Nully-Y, width=1, fill="blue")
        
    print(time.time())   
    root.after(1000,printObstacles)


###MAIN###
printObstacles()

can.pack()
root.mainloop()
