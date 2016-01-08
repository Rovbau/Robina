#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import sin,cos,radians,sqrt



from copy import deepcopy
from time import *
import pickle

class Karte():
    def __init__(self,encoder):
        self.encoder=encoder
        self.RoboPosY=0
        self.RoboPosX=0
        self.RoboPath=[]
        self.global_kurs=0
        self.kompassOld=0
        self.ScanList2=[[-90,0],[-80,0],[-70,0],[-60,0],[-50,0],[-40,0],[-30,0],[-20,0],[-10,0],
                       [0,0],
                       [10,0],[20,0],[30,0],[40,0],[50,0],[60,0],[70,0],[80,0],[90,0]]

    def updateObstacles(self,Obstacles):
        """Obstacles werden in ScanList eingetragen"""

        #print("obstacles: "+str(Obstacles))
        for i in range(len(Obstacles)): 
            for k in range(len(self.ScanList2)):              
                if Obstacles[i][0]==self.ScanList2[k][0]:
         #           print("IF: "+str(self.ScanList2[k][1])+"   "+str(Obstacles[i][1]))
                    self.ScanList2[k][1]=Obstacles[i][1]
        Ausgabe=deepcopy(self.ScanList2)
        return(Ausgabe)
    
    def updateHardObstacles(self,pumperL,pumperR):
        """Status der Stosstange in Karte eintragen"""
        self.pumperL=pumperL
        self.pumperR=pumperR

    def updateRoboPos(self,deltaDist,SteerDiff,KompassCourse):
        """Update Robo Position auf Karte"""

        #RoboSchwerpunkt bis Rad mm
        a=180   
        c=180

        self.global_kurs=KompassCourse
        print("Kompass ist:" +str(KompassCourse))
            
        WinkelDiff=SteerDiff*5.2    #Counts in Winkel umwandeln
        deltaDist=deltaDist*1.3
        print("WinkelDiff ist:" +str(WinkelDiff))

        if SteerDiff != 0:
            #Kosinussatz: Schwerpunkt Wegversatz berechnen
            b=sqrt(pow(a,2)+pow(c,2)-2*a*c*cos(radians(WinkelDiff)))

            #Richtung des Wegversatz in GlobalKurs umrechnen
            self.global_kurs=self.global_kurs+WinkelDiff
            if self.global_kurs>360:
                self.global_kurs=self.global_kurs-360
            if self.global_kurs<0:
                self.global_kurs=360-abs(self.global_kurs)

            self.encoder.clearEncoderLR()   

            #Position des Robo auf Karte updaten
            self.RoboPosY=b*sin(radians(self.global_kurs))+self.RoboPosY
            self.RoboPosX=b*cos(radians(self.global_kurs))+self.RoboPosX


        if SteerDiff == 0 and deltaDist != 0:
            #Position des Robo auf Karte updaten
            self.RoboPosX=deltaDist*sin(radians(self.global_kurs))+self.RoboPosX
            self.RoboPosY=deltaDist*cos(radians(self.global_kurs))+self.RoboPosY

        if time.time()-timeold > 2:
            #Jede Sec Path speichern            
            self.RoboPath.append([round(self.RoboPosX,1),round(self.RoboPosY,1),self.global_kurs])
            
            pickelRoboPath=open( "RoboPath.p", "wb" )
            pickle.dump(self.RoboPath, pickelRoboPath)
            
            timeold = time.time()

    def getRoboPos(self):
        """returns RoboPos X,Y,pose"""
        return(round(self.RoboPosX,1),round(self.RoboPosY,1),self.global_kurs)
    
    def getRoboPath(self):
        """returns RoboPath X,Y"""
        return(self.RoboPath)

    def getObstacles(self):
        """return latest Obstacles"""
        return(self.ScanList2)

    def getZielkurs(self):
        """return Zielkurs 0-360"""
        return(0)
    
    def getPumperStatus(self):
        """return Stosstangen status"""
        return(self.pumperL,self.pumperR)

if __name__ == "__main__":

    K=Karte()
    
    Obstacles=[[-60,110],[-50,110],[20,130],[40,140]]

    K.updateObstacles(Obstacles)
    print(K.getObstacles())

    deltaDist=10
    SteerDiff=0
    KompassCourse=0
    K.updateRoboPos(deltaDist,SteerDiff,KompassCourse)

    deltaDist=5
    SteerDiff=0
    KompassCourse=90
    K.updateRoboPos(deltaDist,SteerDiff,KompassCourse)
    
    print(K.getRoboPos())
    print(K.getRoboPath())








    
    

