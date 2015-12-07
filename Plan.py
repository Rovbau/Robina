# -*- coding: utf-8 -*-
#Plan

#from Karte import *

from  time import *

class Plan():
    def __init__(self,karte):
        self.karte=karte
        #self.navigation=navigation
        Speed=0
        Steer=False

    def getCourse(self,navigation):
        obstacles=self.karte.getObstacles()
        print(obstacles)
        xx=navigation.LueckeInX(80,obstacles)
        return()
        

class Navigation():
    def __init__(self):
        pass
    
    def LueckeInX(self, Dist,ScanList4):
        """Returns aus ScanList ->LueckeList[[Winkel,MinimaleDist]],wenn 3Werte nacheinander grösser "Dist" sind. """
        global SollKurs
        
        ScanCopy3=ScanList4
        LueckeList=[]
        
        for i in range(len(ScanList4)):
            if ScanList4[i][1]>Dist:
                ScanCopy3[i][1]=ScanList4[i][1]
            else:
                ScanCopy3[i][1]=0

        return()      
        for i in range(len(ScanCopy)-2):
            if ScanCopy[i][1]>Dist and ScanCopy[i+1][1]>Dist and ScanCopy[i+2][1]>Dist:
                #Hier wird die MinDist der drei Elemente ermittelt
                Slice=ScanCopy[i:i+2]
                Min=min(Slice, key= lambda t: t[1])
                ScanCopy[i+1][1]=Min[1]
                LueckeList.append(ScanCopy[i+1])
                
        return(LueckeList)

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
        """Returns MIN aus den Mittleren Werten von ScanList->Int"""
        try:
            Slice=ScanList[5:13]
        except:
            print("Slicing not Working")
            return(0)
        Min=min(Slice, key= lambda t: t[1])
        return(Min)

    def Querab(self,ScanList):
        """Wenn 90 OR 80Grad < Dist: Werte bis 0Grad Nullen """
        
        ScanCopy=ScanList[:]
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
        
        ScanCopy=ScanList[:]
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

        ScanCopy=ScanList[:]

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
