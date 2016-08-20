#Programm Zeigt in Tkinter die RoboPos und die Hindernisse an.
#Daten via Socket und Json

import json
import socket
from threading import Thread
from Tkinter import *
import time
import pickle

#Kartennull fuer TK
Nullx=300
Nully=300

#Tkinter 
root=Tk()
root.title ("Hinderniss-Daten")           #Titel de Fensters
root.geometry("700x700+0+0")
can=Canvas(master=root, width=600, height=600, bg="grey")

class Server():
    def __init__(self):
        self.obs = []
        self.path = []
        self.xx = 0

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
        """Returns the data fromm the socket"""            
        #self.xx = self.xx +10
        #self.obs = [[1,1],[2,7],[2,8]]
        #self.path = [[0,0],[40,40],[50,self.xx]]        
        return(self.obs, self.path)

    def clearValues(self):
        self.obs =[]
        self.path = []


class Sichern():
    def __init__(self):
        self.timeold = 0

    def storeFile(self, obst, path):
        """Pickel Daten"""
        filename = "Stube"        
        last_save = time.time()-self.timeold
        
        if filename != "" and last_save > 4:           
            pickelPath=open( "LogRoboWeg-"+filename, "wb" )
            pickle.dump(path+obst, pickelPath)
            pickelPath.close()
            self.timeold = time.time()

 

class Visual():
    def __init__(self, sichern):
        self.Nullx = 300
        self.Nully = 300
        self.obstacles_in_grid = []
        self.position_in_grid = []
        self.sichern = sichern
       
    def printObstacles(self):
        """Zeichne die Hindernisse und RoboPath"""

        Nullx = self.Nullx
        Nully = self.Nully 
        obstacles, path = serv.getNewValues()
        print(obstacles)
        print(path)

        if len(obstacles) != 0:
            self.obstacles_in_grid.extend(obstacles)
            self.position_in_grid.extend(path)
        serv.clearValues()
        can.delete("Point")

        #Save neu Points
        self.sichern.storeFile(self.obstacles_in_grid, self.position_in_grid)

        print("DataPoints: "+str(len(self.obstacles_in_grid))+" "+str(len( self.position_in_grid)))
        
        for pos in self.obstacles_in_grid:
            X=pos[0]
            Y=pos[1]
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
        self.Nullx = self.Nullx + x
        self.Nully = self.Nully + y
        can.delete("Point")
        return
    
###MAIN###

serv = Server()
sichern = Sichern()
visual = Visual(sichern)

print("Init")
#Server lauscher
ThreadScanAllTime=Thread(target=serv.getJsonOby, args=())
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

visual.printObstacles()

#Zeichne Karte und Massstab, Button
buttonL = Button(root, text="Links", fg="blue",command=lambda: visual.setZoom(-100,0))
buttonR = Button(root, text="Rechts", fg="blue",command=lambda: visual.setZoom(100,0))
buttonU = Button(root, text="Unten", fg="blue",command=lambda: visual.setZoom(0,100))
buttonO = Button(root, text="Oben", fg="blue",command=lambda: visual.setZoom(0,-100))
buttonO.pack(side=TOP)
buttonU.pack(side=BOTTOM)
buttonR.pack(side=RIGHT)
buttonL.pack(side=LEFT)

entryIP = Entry(root)
entryIP.pack()
entryIP.insert(10,"Ring entspricht 50 cm")
can.create_oval(Nullx-2,Nully+2,Nullx+2,Nully-2, width=1, fill=None)
can.create_oval(Nullx-50,Nully+50,Nullx+50,Nully-50, width=1, fill=None, outline="gray78")
can.create_oval(Nullx-100,Nully+100,Nullx+100,Nully-100, width=1, fill=None, outline="gray78")
can.create_oval(Nullx-150,Nully+150,Nullx+150,Nully-150, width=1, fill=None, outline="gray78")
filename = entryIP.get()
can.pack()

root.mainloop()
