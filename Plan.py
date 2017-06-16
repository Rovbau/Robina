# -*- coding: utf-8 -*-
#Plan

from  time import *
from copy import deepcopy

from math import sin,cos,degrees,sqrt,atan2
import logging

logging.basicConfig(level=logging.INFO)

class Plan():
    def __init__(self):       
        pass

    def nextZielPattern(self,x,y):
        """Wenn aktuelles Ziel errreicht, next Ziel anfahren"""
        _,dist_to_globalziel = self.calcZieldaten(x,y,0)
        goal = False
        if dist_to_globalziel < 20:
            try:
                neu_ziel = next(self.generator_ziel)
                neu_x , neu_y = neu_ziel
                self.setGlobalZiel(neu_x,neu_y)
            except:
                print("BIN am ZIEL STOPPE")    
                goal = True
        return(self.endziel_x, self.endziel_y, goal)

    def init_generator_ziel(self,ziellist):
        """init Generator mit Zieldaten"""
        self.generator_ziel = self.generiere_ziel(ziellist)
        self.setGlobalZiel(0,0)
        
    def generiere_ziel(self,zielliste):
        """Generator Funktion mit Zieldaten"""
        for next_ziel in zielliste:
            yield(next_ziel)

    def calcZieldaten(self,x,y,pose):
        """Berechne Zieldaten anhand aktueller Pos"""
        #Diff EndzielX/Y von Pos 
        diff = (self.endziel_x - x, self.endziel_y - y)
        #Kartesisch in Polarkoordinaten
        x,y=diff
        dist_to_globalziel=sqrt(pow(x,2)+pow(y,2))
        kurs_to_globalziel=degrees(atan2(y,x))
        return(int(kurs_to_globalziel),int(dist_to_globalziel))

    def setGlobalZiel(self, endziel_x, endziel_y):
        self.endziel_x, self.endziel_y = endziel_x, endziel_y
        
    def getGlobalZiel(self):
        return(self.endziel_x, self.endziel_y)
        
    def nextStep(self,path,x,y,pose):
        """Plane next steer,speed commando"""
        start=path[0]
        zwischenziel=path[7]

        #Diff GridX,GridY von Pos zu Zwischenziel
        diff = (zwischenziel[0]-start[0], zwischenziel[1]-start[1])
        #Kartesisch in Polarkoordinaten
        x,y=diff
        dist_to_zwischenziel=sqrt(pow(x,2)+pow(y,2))
        kurs_to_zwischenziel=degrees(atan2(y,x))
        print("Ist: "+str(start))
        print("Soll: "+str(zwischenziel))
        
        kurs_korr=self.KursDiff(kurs_to_zwischenziel,pose)
        steer,speed=self.SteuerkursInSteerSpeed((kurs_korr , dist_to_zwischenziel))

        print("Kurs: "+str(int(kurs_to_zwischenziel))+
                           " KursKorr: "+str(int(kurs_korr))+" Pose: "+str(int(pose)))
        print("----")
        return(steer,speed)

    def ZuNahe(self,steer,speed,wall_near):
        if wall_near == True:
            steer=0
            speed=-1
            print("ZU NAHE RETOUR")
        return(steer,speed)
            
    def KursDiff(self,Soll,Ist):
        """Diff zwischen zwei Winkel 0-360grad"""
        if Soll>Ist:
            if Soll-Ist>180:
                Winkel=(abs(Ist-Soll)-360)
            else:
                Winkel=Soll-Ist
        else:     
            if Ist-Soll>180:
                Winkel=360-(Ist-Soll)
            else:
                Winkel=Soll-Ist
        return(Winkel)

    def SteuerkursInSteerSpeed(self,steuerkurs):
        """Die eingabe steuerkurs=[zielkurs,Dist] wird in (steer, speed) umgewandelt ->returns (steer,speed)"""
        if steuerkurs[0] > 5:
            steer = 1
        elif steuerkurs[0] < -5:
            steer = -1
        else:
            steer = 0
                
        if steuerkurs[1] > 0:
            speed=1
        else:
            speed=0
            
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
        """Die eingabe steuerkurs=[zielkurs,Dist] wird in (steer, speed) umgewandelt ->returns (steer,speed)"""
        logging.info(steuerkurs[0][0])
        if steuerkurs[0][0] > 10:
            steer = 1
        elif steuerkurs[0][0] < -10:
            steer = -1
        else:
            steer = 0
                
        if steuerkurs[0][1] > 0:
            speed=1
        else:
            speed=0
            
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
                KursAbw=round(self.KursDiff(LueckeList[i][0],IstKurs),1)
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
            ScanListGlobal.append([int(Wert),ScanList[i][1]])
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
                
        return(ScanCopy)


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

    from Karte import *
    
    plan=Plan()
    ziellist =[[11,0],[12,0],[13,0]]
    plan.init_generator_ziel(ziellist)
    
    x , y = 0,0
    plan.nextZielPattern(x,y)
    print(plan.getGlobalZiel())

