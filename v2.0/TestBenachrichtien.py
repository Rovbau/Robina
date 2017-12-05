from Model import *

class Benachrichtigen():

    def __init__(self):

        print(self)
        model.addObserver(self)

    def notify(self):
        print("ich habe neue Daten zum zeigen")

class Gui():

    def __init__(self):
        print(self)
        model.addObserver(self)

    def notify(self):
        print("GUI updaten")
        
model = Model()
nachrichten = Benachrichtigen()
gui = Gui()


model._notifyObservers()

        
        
        
