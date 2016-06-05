#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import smbus
bus = smbus.SMBus(1)

class Sonar():
    def __init__ (self):
        self.PortTrig=38
        self.PortEchoL=40
        self.PortEchoR=8
        OnTime=0
        OffTime=0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortTrig,GPIO.OUT)
        GPIO.output(self.PortTrig,0)
        GPIO.setup(self.PortEchoL,GPIO.IN)
        GPIO.setup(self.PortEchoR,GPIO.IN)
        print("Init Sonar")

    def getScanDist(self,sensor):
        """Distanz von Ultraschall-Sensor (cm) Links oder Rechts"""

        if sensor == "left":
            self.PortEcho=self.PortEchoL
        elif sensor == "right":
            self.PortEcho=self.PortEchoR
        else:
            print("No Sensor on Port"+str(sensor))
        Distance=0
        Durchschnitt=0
        ErrScan=False
        dist_old=0
        for i in range(5):
            OnTime=0
            OffTime=0
            
            #Start Puls
            GPIO.output(self.PortTrig,1)
            time.sleep(0.00002)
            GPIO.output(self.PortTrig,0)
            time.sleep(0.00022)

            #Warte Echo
            PulsStart=time.time()
            while GPIO.input(self.PortEcho)==0:
                if OnTime-PulsStart>1:
                    print("Fehler Sonar RE-Init")
                    ErrScan=True
                    break
                OnTime=time.time()    
            while GPIO.input(self.PortEcho)==1:
                if OffTime-PulsStart>1:
                    print("Fehler Sonar RE-Init")
                    ErrScan=True
                    break
                OffTime=time.time()

            PulsDauer=OffTime-OnTime
            Distance=PulsDauer*17000
            Distance=round(Distance,1)

            #Sleeptime for Sonar
            time.sleep(0.03)
            
            #Fehlerkontrolle
            if Distance > 600 or Distance < 1:
                continue
            
            if abs(Distance - dist_old)<4:
                Durchschnitt=(Distance+dist_old)/2
                break
            else:
                dist_old=Distance
                continue

        return(int(Durchschnitt),ErrScan)


    def GetADC(self,ADC_cannel):
            """Returns A/D Wert an Port 0. Distanz Infrarot (cm)"""
            Ref=3.3
            Adress=0x48
            
            bus.write_byte(0x48,0x40+ADC_cannel)         #PCF8591, Adress 0x48,Commando=1000000
            
            Rohdaten=bus.read_byte(0x48)                #Old Data Adresse,
            Rohdaten=bus.read_byte(0x48)
            Messdaten=(round(Ref/255*Rohdaten,3))        #Korrekte Spann. berechen
            
            Dist=int(round((1/(Messdaten*0.0088+0.003)-22),1))
            ErrScan=False
            return(Dist, ErrScan)

    def GetBatSpann(self):
            """Returns A/D Wert an Port 1. Batt. spannung (V)"""
            Ref=3.3
            Adress=0x48
            ADCCannel=1
            
            bus.write_byte(0x48,0x40+ADCCannel)               #PCF8591, Adress 0x48,Commando=1000001
            
            Rohdaten=bus.read_byte(0x48) #Adresse, Dummy Read alte Daten
            Rohdaten=bus.read_byte(0x48) #Adresse, 
            Messdaten=round(Ref/255*Rohdaten,3)       #Korrekte Spann. berechen

            Dist=round((Messdaten*5),2)
            ErrScan=False
            return(Dist, ErrScan)

if __name__ == "__main__":

    s=Sonar()
    while True:
        print("Front")
        print(s.GetADC(0))

        print("Left")
        print(s.GetADC(2))

        print("Right")
        print(s.GetADC(3))

        print("Left-Sonar")
        print(s.getScanDist("left"))

        print("Batt.-Spannung")
        print(s.GetBatSpann())
        print("***********")
        time.sleep(2.0)
