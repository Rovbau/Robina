#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import sin,cos,radians,sqrt
from copy import deepcopy
import time
import pickle

class Karte():
    def __init__(self,encoder):
        self.encoder=encoder
        self.RoboPosY=10
        self.RoboPosX=10
        self.RoboPath=[]
        self.globalObstaclesList=[]
        self.global_kurs=0
        self.kompassOld=0
        self.timeold=0

    def updateObstacles(self, Obstacles):
        """Obstacles werden in ScanList eingetragen"""

        for Obstacle in Obstacles:            
            #Wandeln Winkeldaten für Globalberechnung: -90zu+90 und +90zu-90 0=0
            #ScanList[i][0]=degrees(asin(sin(radians(ScanList[i][0])+radians(180))))

            Dx = Obstacle[0]
            Dy = Obstacle[1]

            #Drehmatrix für X, Returns Global Hindernis Position
            X=(Dx*cos(radians(self.global_kurs))-Dy*(-sin(radians(self.global_kurs))))+self.RoboPosX

            #Drehmatrix für Y, Returns Global Hindernis Position
            Y=(Dx*sin(radians(self.global_kurs))+Dy*(-cos(radians(self.global_kurs))))+self.RoboPosY

            self.globalObstaclesList.append([X,Y])

    def getGlobalObstaclesListDiff(self):
        self.globalObstaclesList=[[60,60],[50,50],[0,130],[0,140]]
        return(self.globalObstaclesList)
    
    def updateHardObstacles(self,bumperL,bumperR):
        """Status der Stosstange in Karte eintragen"""
        self.pumperL = bumperL
        self.pumperR = bumperR
        if bumperL:
            self.updateObstacles([(-150, 0)])
        if bumperR:
            self.updateObstacles([(150, 0)])

    def updateRoboPos(self,deltaDist,SteerDiff,KompassCourse):
        """Update Robo Position auf Karte"""

        #RoboSchwerpunkt bis Rad cm
        a=18  
        c=18
            
        WinkelDiff=SteerDiff*5.2    #Counts in Winkel umwandeln
        deltaDist=deltaDist*1.3
        print(WinkelDiff)

        if abs(SteerDiff) >= 1:
            #Kosinussatz: Schwerpunkt Wegversatz berechnen
            b=sqrt(pow(a,2)+pow(c,2)-2*a*c*cos(radians(WinkelDiff)))

            #Richtung des Wegversatz in GlobalKurs umrechnen
            self.global_kurs=KompassCourse
            self.global_kurs=self.global_kurs+WinkelDiff
            if self.global_kurs>360:
                self.global_kurs=self.global_kurs-360
            if self.global_kurs<0:
                self.global_kurs=360-abs(self.global_kurs)   

            #Delta x,y anhand SteerDiff berrechnen
            Dx=b*cos(radians((180-abs(WinkelDiff))/2))
            Dy=b*sin(radians((180-abs(WinkelDiff))/2))
            
            #Position des Robo auf Karte updaten
            self.Drehmatrix(Dx,Dy)
            self.encoder.clearEncoderLR()

        if  deltaDist != 0 and SteerDiff == 0:        
            #Position des Robo auf Karte updaten
            Dx=0
            Dy=deltaDist
            
            self.Drehmatrix(Dx,Dy)
            self.encoder.clearEncoderDist()
            
        if time.time()-self.timeold > 2:
            #Jede Sec Path speichern            
            self.RoboPath.append([round(self.RoboPosX,1),round(self.RoboPosY,1),self.global_kurs])
            
            pickelRoboPath=open( "RoboPath.p", "wb" )
            pickle.dump(self.RoboPath, pickelRoboPath)
            
            self.timeold = time.time()

    def Drehmatrix(self,Dx,Dy):
            #Drehmatrix für X, Returns Global Hindernis Position
            self.RoboPosX=(Dx*cos(radians(self.global_kurs))+Dy*(sin(radians(self.global_kurs))))+self.RoboPosX
            #Drehmatrix für Y, Returns Global Hindernis Position
            self.RoboPosY=(-Dx*sin(radians(self.global_kurs))+Dy*(cos(radians(self.global_kurs))))+self.RoboPosY


    def getRoboPos(self):
        """returns RoboPos X,Y,pose"""
        return(round(self.RoboPosX,1),round(self.RoboPosY,1),self.global_kurs)

    def setRoboPosZero(self):
        self.RoboPosX=0
        self.RoboPosY=0
    
    def getRoboPath(self):
        """returns RoboPath X,Y"""
        return(self.RoboPath)

    def getObstacles(self):
        """return latest Obstacles"""
        return(self.globalObstaclesList)

    def getZielkurs(self):
        """return Zielkurs 0-360"""
        return(0)
    
    def getPumperStatus(self):
        """return Stosstangen status"""
        return(self.pumperL,self.pumperR)

if __name__ == "__main__":

    enc=1
    K=Karte(enc)
    
    Obstacles=[[60,60],[50,50],[0,130],[0,140]]

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








    
    

