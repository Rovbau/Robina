# -*- coding: utf-8 -*-
#Plan

from  time import *
from copy import deepcopy
import Kompass
import math

class Plan():
    def __init__(self,karte,navigation):
        self.karte=karte
        self.navigation=navigation
        speed=0
        steer=None

    def getCourse(self):
        #Obstacles aus karte lesen
        obstacles=self.karte.getObstacles()
        
        #Wenn Vorne kein Platz retour
        steer,speed=self.navigation.MinInFront(obstacles)
        if speed == -1:
            return(steer,speed)

        #Wenn Pumper Hinderniss erkannt retour
        pumpL,pumpR=self.karte.getPumperStatus()
        if pumpL == True:
            return(0,-1)
        if pumpR == True:
            return(0,-1)
        
        #Bei Hinderniss R oder L nicht drehen
            #obstacles=self.navigation.Querab(obstacles)
        
        #Parallele Wand erkennen
        obstacles=self.navigation.WandParallel(obstacles)
        
        #Suche Luecke in Dist
        obstacles=self.navigation.LueckeInX(80,obstacles)

        sollkurs=self.karte.getZielkurs()
        istkurs=Kompass.getKompass()
        
        #Lokale Koordinaten in Globale umwandeln
        LueckeList=self.navigation.LokalZuGlobal(istkurs,obstacles)
        
        #Suche beste Luecke um nach Zielkurs zu kommen       
        to_steer=self.navigation.BesteLueckeKompass(sollkurs,istkurs,obstacles)      
        #print(to_steer)
        
        #Ausgabe der Motor Comands steer und speed
        steer,speed=self.navigation.SteuerkursInSteerSpeed(to_steer)
        #print(steer,speed)
        
        return(steer,speed)
        

class Navigation():
    def __init__(self):
        pass
    
    def LueckeInX(self, dist,scanList):
        """Returns aus scanList ->LueckeList[[Winkel,MinimaleDist]],wenn 3Werte nacheinander grösser "Dist" sind. """
        
        scanCopy=deepcopy(scanList)
        lueckeList=[]
        
        for i in range(len(scanList)):
            if scanList[i][1]>dist:
                scanCopy[i][1]=scanList[i][1]
            else:
                scanCopy[i][1]=0
     
        for i in range(len(scanCopy)-2):
            if scanCopy[i][1]>dist and scanCopy[i+1][1]>dist and scanCopy[i+2][1]>dist:
                #Hier wird die MinDist der drei Elemente ermittelt
                slicen=scanCopy[i:i+2]
                minimum=min(slicen, key= lambda t: t[1])
                scanCopy[i+1][1]=minimum[1]
                lueckeList.append(scanCopy[i+1])
                
        return(lueckeList)

    def SteuerkursInSteerSpeed(self,steuerkurs):
        """Die eingabe [Steuerkurs,Dist] wird in (steer, speed) umgewandelt ->returns (steer,speed)"""
        if steuerkurs[0][0] > 0:
            steer=1
        else:
            steer=-1

        if steuerkurs[0][1] > 0:
            speed=1
        else:
            speed=-1
        return(steer,speed)
        
    def BesteLueckeKompass(self,SollKurs,IstKurs,LueckeList):
        """Aus LueckeList -> Returns Steuerkurs, Steuerkurs wird anhand SollKurs ZU IstKurs optimiert
        Wenn LueckeList leer -> Returns Kurve 45/-45grad""" 
        if len(LueckeList)==0:
                #Keine Luecke, return 45/-45° Kurs optimiert
                #LueckeList=self.LokalZuGlobal(IstKurs,[[-45,10],[45,10]])
                #Drehen=self.BesteLueckeKompass(SollKurs,IstKurs,LueckeList)
                Drehen=[[45,30]]
                return(Drehen)
                    
        MinDiff=360
        Steuerkurs=[]
        
        for i in range(len(LueckeList)):
            Diff=self.KursDiff(LueckeList[i][0],SollKurs)
            if abs(Diff)<abs(MinDiff):
                KursAbw=self.KursDiff(LueckeList[i][0],IstKurs)
                Steuerkurs=[[KursAbw,LueckeList[i][1]]]
                MinDiff=Diff
        return(Steuerkurs)
        

    def BesteLueckeKurs(self,LueckeList):
        """Returns beste Luecke in Fahrtrichtung (Winkel,Dist)"""
        
        SteuerkursList=LueckeList
        
        if len(SteuerkursList)==0:
                return([[90,10]])
       
        AbsMin=[[360,0]]
        for i in range(len(SteuerkursList)):
                if abs(SteuerkursList[i][0])<abs(AbsMin[0][0]):
                        AbsMin=[SteuerkursList[i]]
        return(AbsMin)


    def LokalZuGlobal(self,Kurs,ScanList):
        """ScanWinkelList in GlobalKursGradeListe umwandeln"""
        ScanListGlobal=[]
        
        for i in range(len(ScanList)):
            Wert=Kurs+ScanList[i][0]
            if Wert>360:
                Wert=Wert-360
            if Wert<0:
                Wert=360-abs(Wert)
            ScanListGlobal.append([Wert,ScanList[i][1]])
        return(ScanListGlobal)

        
    def KursDiff(self,SollRichtung,Kompass):
        """Diff zwischen zwei Winkel 0-360grad"""
        if SollRichtung>Kompass:
            if SollRichtung-Kompass>180:
                Winkel=(abs(Kompass-SollRichtung)-360)
            else:
                Winkel=SollRichtung-Kompass
        else:     
            if Kompass-SollRichtung>180:
                Winkel=360-(Kompass-SollRichtung)
            else:
                Winkel=SollRichtung-Kompass
        return(Winkel)

    def MinInFront(self,ScanList):
        """Returns MIN aus den Mittleren Werten von ScanList->Returns steer=0 retour=-1"""
        try:
            Slice=deepcopy(ScanList[5:13])
        except:
            print("Slicing not Working")
            return(0)
        Min=min(Slice, key= lambda t: t[1])
        if Min[1]<25:
            return(0,-1)
        else:
            return(0,1)

    def Querab(self,ScanList):
        """Wenn 90 OR 80Grad < Dist: Werte bis 0Grad Nullen """
        
        ScanCopy=deepcopy(ScanList)
        Dist=30

        Laenge=len(ScanList)

        if ScanList[0][1]<Dist or ScanList[1][1]<Dist:
            for i in range(int(Laenge/2)):
                ScanCopy[i][1]=0

        if ScanList[Laenge-2][1]<Dist or ScanList[Laenge-1][1]<Dist:
            for i in range(Laenge-1, int(Laenge/2), -1):
                ScanCopy[i][1]=0
                
        ScanList=ScanCopy[:]
        return(ScanList)

    def WandParallel(self,ScanList):
        """Mit TrigoMath paralle Wand in DIST erkennen und ScanList anpassen"""
        
        ScanCopy=deepcopy(ScanList)
        Dist=30
        
        for i in range(len(ScanCopy)):

            Trigo=10+(Dist/math.cos(math.radians(90-abs(ScanCopy[i][0]))))
            if Trigo>100:
                Trigo=100
            
            if ScanCopy[i][1]<Trigo:
                ScanCopy[i][1]=0
                #print("Wand")
            #else:
                #print("----")

        ScanList=ScanCopy[:]
        return(ScanList)


    def FlacheHindernisse(self,ScanList,Alarm):

        ScanCopy=deepcopy(ScanList)

        Laenge=len(ScanList)
        if Alarm=="L":
            for i in range(int(Laenge/2)):
                ScanCopy[i][1]=0
        if Alarm=="R":
            for i in range(Laenge-1, int(Laenge/2), -1):
                ScanCopy[i][1]=0

        RueckmeldungAlarm=False
        ScanList=ScanCopy[:]
        print("Flaches Hinderniss bei:"+str(Alarm))
        return(ScanList,RueckmeldungAlarm)        
        

    def Ausweichen(self,MotorOby,SollKurs, *arg):
        """Bei Kontakt ausweiche Manoever einleiten"""
        AlarmL,AlarmR=GetAlarme()
        RueckmeldungAlarm=""

        
        if AlarmL==True and AlarmR==False:
                print("Ausweichen L")
                EncoderClear()
                #MotorOby.RadCorr(10)
                MotorOby.Drive(-15)
                MotorOby.Kurve(30)
                RueckmeldungAlarm="L"
        elif AlarmR==True and AlarmL==False:
                print("Ausweichen R")
                EncoderClear()
                #MotorOby.RadCorr(-10)
                MotorOby.Drive(-15)
                MotorOby.Kurve(-30)
                RueckmeldungAlarm="R"

        elif AlarmR==True and AlarmL==True:
                print("Ausweichen BestKurs")
                IstKurs=self.GetKompass()
                LueckeList=self.LokalZuGlobal(IstKurs,[[-45,0],[45,0]])
                Drehen=self.BesteLueckeKompass(SollKurs,IstKurs,LueckeList)

                if Drehen[0][0]>=0:
                        MotorOby.RadCorr(10)
                else:
                        MotorOby.RadCorr(-10)
                MotorOby.Drive(-15)
                MotorOby.Kurve(Drehen[0][0])
                RueckmeldungAlarm="LR"
                
        elif arg==("Block",):
                MotorOby.Drive(-15)
                
        elif arg==("ZuNah",):
                MotorOby.Drive(-20)

        ClearAlarm()
        return(RueckmeldungAlarm)

    def PrintList(self,LueckeList):
        x=[]
        for i in range(len(LueckeList)-1):
            x.append(LueckeList[i][0])
        print(x)

    def Grafik(self,ScanList):
        """Ausgabe der ScanList als PsydoGrafik"""
        for i in range(len(ScanList)):
            Dist=int(ScanList[i][1]/10)
            if Dist==0:
                print("-")
            else:
                print(Dist*"*")
        

if __name__ == "__main__":

    N=Navigation()
    K=Karte()
    Plan=Plan()
    Plan.getCourse()
