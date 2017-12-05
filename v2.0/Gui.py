import json
import socket
from threading import Thread
from Tkinter import *
import tkFileDialog
import time
import pickle

class Gui():

    def __init__(self, model, controller):
        self.shown = False
        self.xOffset = 0
        self.yOffset = 0
        self.canvasWidth = 600
        self.canvasHeight = 600
        self.controller = controller
        self.root, self.can = self._init()
        self.model = model
        model.addObserver(self)

    def show(self):
        self.shown = True
        self._drawRadar()
        self.root.mainloop()

    def hide(self):
        self.root.destroy()
        self.shown = False

    def notify(self):
        print('gui notified')
        if self.shown:
            self._drawRadar()

    def _init(self):
        #Tkinter 
        root=Tk()
        root.title ("Hinderniss-Daten")           #Titel de Fensters
        root.geometry("700x800+0+0")
        can=Canvas(master=root, width=self.canvasWidth, height=self.canvasHeight, bg="grey")
        buttonL = Button(root, text="Links", fg="blue", command=lambda: self._moveOffset(-100,0))
        buttonR = Button(root, text="Rechts", fg="blue", command=lambda: self._moveOffset(100,0))
        buttonU = Button(root, text="Unten", fg="blue", command=lambda: self._moveOffset(0,-100))
        buttonO = Button(root, text="Oben", fg="blue", command=lambda: self._moveOffset(0,100))
        buttonMenu = Button(root, text="Load", fg="blue", command= lambda: self._load())
        buttonClear = Button(root, text="Clear", fg="blue", command= lambda: self._clear())
        buttonConnect = Button(root, text="Connect", fg="blue", command= lambda: self._connect())
        
        buttonO.pack(side=TOP)
        buttonConnect.pack(side=BOTTOM)
        buttonMenu.pack()
        buttonClear.pack()
        buttonU.pack(side=BOTTOM)
        buttonR.pack(side=RIGHT)
        buttonL.pack(side=LEFT)

        self.coordDisplay = Entry(root, width= 30)
        self.coordDisplay.pack()
        self.coordDisplay.insert(0,"Ring entspricht 50 cm")

        label = Label(root)
        label.pack()
        can.bind("<Button-1>", lambda(event): self._updateClickCoords(event))

        xCenter, yCenter = self._transform(0, 0)
    
        can.create_oval(xCenter-2,   yCenter+2,   xCenter+2,   yCenter-2,   width=1, fill=None, tag="Radar")
        can.create_oval(xCenter-50,  yCenter+50,  xCenter+50,  yCenter-50,  width=1, fill=None, outline="gray78", tag="Radar")
        can.create_oval(xCenter-100, yCenter+100, xCenter+100, yCenter-100, width=1, fill=None, outline="gray78", tag="Radar")
        can.create_oval(xCenter-150, yCenter+150, xCenter+150, yCenter-150, width=1, fill=None, outline="gray78", tag="Radar")

        can.pack()
        return(root, can)

    def _moveOffset(self, x, y):
        self.xOffset += x
        self.yOffset += y
        self.can.move("Radar", x, y)
        self.can.move("Point", x, y)

    def _load(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",
                                                      filetypes = (("pickels","*.p"),("all files","*.*")))
        if fileName != '':
            self.controller.load(fileName)
            self.controller.stop()

    def _clear(self):
        # clear model state
        pass

    def _connect(self):
        self.controller.start()

    def _updateClickCoords(self, event):
        point_id = self.can.find_closest(event.x, event.y)
        item_color = self.can.itemcget(point_id, "fill")
        xPos, yPos = self._transformBack(event.x, event.y)
        if item_color == "red":
            self.coordDisplay.delete(0, 'end')
            self.coordDisplay.insert(0,"Hinderniss bei X: "+str(xPos)+" "+"Y: "+str(yPos))
        else:   
            self.coordDisplay.delete(0, 'end')
            self.coordDisplay.insert(0,"Koordinate bei X: "+str(xPos)+" "+"Y: "+str(yPos))

    def _drawRadar(self):
        self.can.delete("Point")
        for obstacle in self.model.data.obstacles:
            x, y = self._transform(obstacle[0], obstacle[1], correction = 10)
            #Obstacle Farbe nach Anzahlhits
            anzahl_hit = min(200, obstacle[2] * 5)
            obst_color = '#%02x%02x%02x' % (200, 200-anzahl_hit, 200-anzahl_hit)
            #Zeichne Hindernisspunkte Global ein
            self.can.create_rectangle(x - 5, y + 5, x + 5, y - 5, width=1, fill=obst_color,tag="Point")   

        for node in self.model.data.path:
            x, y = self._transform(node[0], node[1])
            #Zeichne Path Global ein
            self.can.create_oval(x - 15, y + 15, x + 15, y - 15, width=1, fill=None,tag="Point")

        for node in self.model.data.solvedPath:
            x, y = self._transform(node[0], node[1], correction = 10)
            #Zeichne A*-Wegpunkte Global ein 
            self.can.create_oval(x - 3, y + 3, x + 3, y - 3, width=1, fill="green",tag="Point")

    def _offset(self):
        return((self.canvasWidth / 2) + self.xOffset, (self.canvasHeight / 2) + self.yOffset)

    def _transform(self, x, y, correction = 1):
        xOffset, yOffset = self._offset()
        return(xOffset + x * correction, yOffset + y * correction)

    def _transformBack(self, x, y):
        xOffset, yOffset = self._offset()
        return(x - xOffset, y - yOffset)
