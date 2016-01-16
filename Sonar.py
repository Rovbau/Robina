#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import smbus
bus = smbus.SMBus(1)

class Sonar():
    def __init__ (self):
        self.PortTrig=38
        self.PortEcho=40
        OnTime=0
        OffTime=0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortTrig,GPIO.OUT)
        GPIO.output(self.PortTrig,0)
        GPIO.setup(self.PortEcho,GPIO.IN)
        print("Init Sonar")

    def GetScanDist(self):
        """Distanz von Ultraschall-Sensor (cm)"""
        Distance=0
        Durchschnitt=0
        ErrScan=0
        for i in range(3):
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
                    break
                OnTime=time.time()    
            while GPIO.input(self.PortEcho)==1:
                if OffTime-PulsStart>1:
                    print("Fehler Sonar RE-Init")
                    break
                OffTime=time.time()

            PulsDauer=OffTime-OnTime
            Distance=PulsDauer*17000
            Distance=round(Distance,1)
            
            #Fehlerkontrolle
            if Distance<600 and Distance>1:
                Durchschnitt=Distance+Durchschnitt
            else:
                continue

            time.sleep(0.0300)
            
        Durchschnitt=int(round(Durchschnitt/3,1))
        return(Durchschnitt,ErrScan)


    def GetADC(self):
            """Returns A/D Wert an Port 0. Distanz Infrarot (cm)"""
            Ref=3.3
            Adress=0x48
            ADCCannel=0
            
            bus.write_byte(0x48,0x40+ADCCannel)         #PCF8591, Adress 0x48,Commando=1000000
            
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
    print(s.GetADC())
    
