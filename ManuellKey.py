from threading import Thread
from time import *
import sys
#import msvcrt
#import getch

class Manuell():
    def __init__(self):
        self.speed = 0
        self.steer = 0
        print("Init Manuell")
        
    def runManuell(self):
        
        while True:
            #comm = msvcrt.getch()
            comm = sys.stdin.read(2)
            #comm = getch.getch()
            comm = comm[0]
            #comm = input()
            print("Taste: "+str(comm))

            if comm == "8":
                speed=1
                steer=0
            elif comm == "6":
                speed=0
                steer=-1
            elif comm == "4":
                speed=0
                steer=1
            elif comm == "0":
                speed=0
                steer=0
            elif comm == "2":
                speed=-1
                steer=0
            elif comm == "1":
                speed=-1
                steer=1
            elif comm == "3":
                speed=-1
                steer=-1            
            else:
                speed=0
                steer=0
            self.speed = speed
            self.steer = steer

    def getManuellCommand(self):
        return(self.steer,self.speed)
        
if __name__ == "__main__":
    
    man = Manuell()

    ThreadEncoder=Thread(target=man.runManuell,args=())
    ThreadEncoder.daemon=True
    ThreadEncoder.start()

    while True:
        print("Main")
        print(man.getManuellCommand())
        sleep(2)
    

