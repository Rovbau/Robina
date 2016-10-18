#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import sin,cos,radians,degrees,sqrt,pi
from copy import deepcopy
import time
import cPickle as pickle

class Karte():
    def __init__(self,encoder):
        self.encoder=encoder
        self.RoboPosY=0
        self.RoboPosX=0
        self.RoboPath=[]
        self.globalObstaclesList=[]
        self.global_kurs=0
        self.kompassOld=0
        self.timeold=0

    def updateObstacles(self, Obstacles):
        """Obstacles werden in Karte eingetragen"""
        for Obstacle in Obstacles:            
            #Wandeln Winkeldaten für Globalberechnung: -90zu+90 und +90zu-90 0=0
            #ScanList[i][0]=degrees(asin(sin(radians(ScanList[i][0])+radians(180))))

            Dx = Obstacle[0]
            Dy = Obstacle[1]

            #Drehmatrix für X, Returns Global Hindernis Position
            X=(Dx*cos(radians(self.global_kurs))+Dy*(-sin(radians(self.global_kurs))))+self.RoboPosX
            #Drehmatrix für Y, Returns Global Hindernis Position
            Y=(Dx*sin(radians(self.global_kurs))+Dy*(cos(radians(self.global_kurs))))+self.RoboPosY

            self.globalObstaclesList.append([int(X),int(Y)])
    
    def updateHardObstacles(self,pumperL,pumperR):
        """Status der Stosstange in Karte eintragen"""
        if pumperL:
            self.updateObstacles([(10, 20)])
            self.updateObstacles([(10, 10)])
            self.updateObstacles([(10, 0)])
        if pumperR:
            self.updateObstacles([(10, -20)])
            self.updateObstacles([(10, -10)])
            self.updateObstacles([(10, 0)])

    def updateRoboPos(self,deltaL,deltaR,KompassCourse):
        """Update Robo Position auf Karte"""
        #print("Counts: "+str(deltaL)+" "+str(deltaR))
        #RoboSchwerpunkt bis Rad cm
        a=13.0 
        c=13.0
        Radstand=a+c
        countsRadGross=32

        #Werte Uebernehmen: Counts in (cm) umrechnen
        deltaL=deltaL*((5.5*pi)/countsRadGross)           #(Radumfang)/counts
        deltaR=deltaR*((5.5*pi)/countsRadGross)           #(Radumfang)/counts
        WinkelDiff=degrees((deltaR-deltaL)/Radstand)      #Raddist/Radstandbreite
        
        self.global_kurs=self.global_kurs+WinkelDiff        #Global Kurs anhand Weg berechnen
        if self.global_kurs>360:
            self.global_kurs=self.global_kurs-360
        if self.global_kurs<0:
            self.global_kurs=360-abs(self.global_kurs)            
        global_kurs_radiant=radians(self.global_kurs)
        #global_kurs_radiant=0
        #self.global_kurs=KompassCourse                           
        #deltaHintenDist=deltaDist*((8.5*pi)/20)                    #(RadumfangHinten)/counts


        if deltaL != deltaR:
            da=(deltaR-deltaL)/Radstand     #Drehwinkel in  [rad]
            ds=(deltaL+deltaR)/2            #Mittler Strecke von L und R

            #delta X und Y berechnen nach einer Kurve Dx->Waagerecht Dy->senkrecht
            dx=(ds/da)*(cos((pi/2)+global_kurs_radiant-da)+cos(global_kurs_radiant-(pi/2)))
            dy=(ds/da)*(sin((pi/2)+global_kurs_radiant-da)+sin(global_kurs_radiant-(pi/2)))
            
            #print("STEER: "+str(round(dx,3))+"  "+str(round(dy,3))+"  "+str(deltaL)+str(deltaR))
            
            #Position des Robo auf Karte updaten
            self.Drehmatrix(dx,dy)
            #Clear Encoder    
            self.encoder.clearEncoderLR()

        else:       
            dx=deltaR*cos(global_kurs_radiant)
            dy=deltaL*sin(global_kurs_radiant)
            #print("DIST : "+str(round(dx,2))+"  "+str(round(dy,2))+"  "+str(deltaL)+str(deltaR))
            
            #Position des Robo auf Karte updaten
            self.Drehmatrix(dx,dy)
            #Clear Encoder    
            self.encoder.clearEncoderLR()
            
            #Drehmatrix für X, Returns Global Hindernis Position
            #self.RoboPosX=(Dx*cos(radians(self.global_kurs))+Dy*(sin(radians(self.global_kurs))))+self.RoboPosX
            #Drehmatrix für Y, Returns Global Hindernis Position
            #self.RoboPosY=(-Dx*sin(radians(self.global_kurs))+Dy*(cos(radians(self.global_kurs))))+self.RoboPosY

    def Drehmatrix(self,dx,dy):
        self.RoboPosX=self.RoboPosX+dx
        self.RoboPosY=self.RoboPosY+dy
        
    def saveRoboPath(self):
        """Pickel Robos Path every Xsec."""
        if time.time()-self.timeold > 2:          
            self.RoboPath.append([round(self.RoboPosX,1),round(self.RoboPosY,1)])
            pickelRoboPath=open( "RoboPath.p", "wb" )
            pickle.dump(self.RoboPath, pickelRoboPath)
            pickelRoboPath.close()
            self.timeold = time.time()

    def getRoboPos(self):
        """returns RoboPos X,Y,pose"""
        return(round(self.RoboPosX,1),round(self.RoboPosY,1),round(self.global_kurs,2))

    def setRoboPosZero(self,x,y):
        """Set Robo Position zb bei Start"""
        self.RoboPosX=x
        self.RoboPosY=y
    
    def getRoboPath(self):
        """returns RoboPath X,Y"""
        return(self.RoboPath)

    def getObstacles(self):
        """return latest Obstacles"""
        ausgabeObstacle = self.globalObstaclesList
        self.globalObstaclesList = []
        return(ausgabeObstacle)

    def getZielkurs(self):
        """return Zielkurs 0-360"""
        return(0)
    
    def getPumperStatus(self):
        """return Stosstangen status"""
        return(self.pumperL,self.pumperR)

if __name__ == "__main__":

    from Encoder import *
    enc=Encoder()
    K=Karte(enc)
    
    Obstacles=[[60,60],[50,50],[0,130],[0,140]]

    K.updateObstacles(Obstacles)
    print(K.getObstacles())

    deltaDist=0
    SteerDiff=0
    deltaDistRad=10
    deltaL=-100
    deltaR=0
    KompassCourse=0
    K.updateRoboPos(deltaL,deltaR,KompassCourse)
    print(K.getRoboPos())
    
    deltaL=-60
    deltaR=0
    KompassCourse=0
    K.updateRoboPos(deltaL,deltaR,KompassCourse)  
    print(K.getRoboPos())
    
    print(K.getRoboPath())








    
    

