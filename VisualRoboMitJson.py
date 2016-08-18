#Programm Zeigt in Tkinter die RoboPos und die Hindernisse an.
#Daten via Socket und Json

import json
import socket
from threading import Thread
from Tkinter import *
import time

#Kartennull fuer TK
Nullx=200
Nully=380

#Tkinter 
root=Tk()
root.title ("Hinderniss-Daten")           #Titel de Fensters
root.geometry("700x700+0+0")
can=Canvas(master=root, width=600, height=600, bg="grey")

class Server():
    def __init__(self):
        self.obs = []
        self.path = []

    def getJsonOby(self):
        """load a new Json Objekt"""   
        try:
            while True:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.bind(("", 50000)) 

                daten, addr = s.recvfrom(1024)
                nachricht = json.loads(daten)
                
                self.obs = nachricht["Obstacles"]
                self.path = nachricht["Path"]
        finally: 
            s.close()
        return()

    def getNewValues(self):
        print(self.obs)
        return(self.obs, self.path)

    def clearValues(self):
        self.obs =[]
        self.path = []

class Visual():
    def __init__(self):
        self.Nullx = 100
        self.Nully = 100
        self.obstacles_in_grid = [[24,16],[15,5],[20,20]]
        self.position_in_grid = []
        
        
    def printObstacles(self):
        """Zeichne die Hindernisse und RoboPath"""

        Nullx = self.Nullx
        Nully = self.Nully 
        obstacles, path = serv.getNewValues()
        print(obstacles)


        self.obstacles_in_grid.append(obstacles)
        self.position_in_grid.append(path)
        serv.clearValues()
       
        #obstacles_in_grid = [[2,10],[5,5],[20,20]]
        #position_in_grid = [[3,13],[18,18],[22,22]]
        print(self.obstacles_in_grid)
        
        for pos in self.obstacles_in_grid:
            print(pos)
            X=pos[0]*10
            Y=pos[1]*10
            #Zeichne Hindernisspunkte Global ein 
            can.create_rectangle(Nullx+X-5,Nully-Y+5,Nullx+X+5,Nully-Y-5, width=1, fill="red",tag="Point")

        for pos in self.position_in_grid:
            X=pos[0]
            Y=pos[1]
            #Zeichne Path Global ein 
            can.create_oval(Nullx+X-15,Nully-Y+15,Nullx+X+15,Nully-Y-15, width=1, fill=None,tag="Point")

        root.after(1500,visual.printObstacles)

    def setZoom(self,x,y):
        """Kartenausschnitt Verschieben"""
        print("Verschiebe Karte")
        self.Nullx = x
        self.Nully = y
        can.delete("Point")
        return
    
###MAIN###

serv = Server()
visual = Visual()

ThreadScanAllTime=Thread(target=serv.getJsonOby, args=())
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()


visual.printObstacles()


buttonL = Button(root, text="Links", fg="blue",command=lambda: visual.setZoom(200,200))
buttonR = Button(root, text="Rechts", fg="blue",command=lambda: visual.setZoom(200,600))
buttonU = Button(root, text="Unten", fg="blue",command=lambda: visual.setZoom(100,400))
buttonO = Button(root, text="Oben", fg="blue",command=lambda: visual.setZoom(400,400))
buttonL.pack(side=TOP)
buttonR.pack(side=BOTTOM)
buttonU.pack(side=RIGHT)
buttonO.pack(side=LEFT)

entryIP = Entry(root)
entryIP.pack()
can.create_oval(Nullx-2,Nully+2,Nullx+2,Nully-2, width=1, fill="black")
can.create_oval(Nullx-50,Nully+50,Nullx+50,Nully-50, width=1, fill=None)
can.create_oval(Nullx-100,Nully+100,Nullx+100,Nully-100, width=1, fill=None)
can.create_oval(Nullx-150,Nully+150,Nullx+150,Nully-150, width=1, fill=None)

can.pack()

root.mainloop()
