# -*- coding: utf-8 -*-
#Encoder
#Programm fragt Radencoder L/R und DistGeber an Robo ab.
#Ausgabe von Distanz und Abweichung der Räder

from time import sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Encoder():
    def __init__(self):
        """init aller Ports, clears all counts"""
        self.PortEncoderL=36
        self.PortEncoderR=32
        self.PortEncoderH=7
        self.TasteL=13
        self.TasteR=15
        self.portRoteTaste=37

        self.PortLRueck=29
        self.PortRRueck=33

        self.WegCount=0
        self.DiffCount=0

        self.AlarmL=False
        self.AlarmR=False
    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortEncoderL,GPIO.IN)
        GPIO.setup(self.PortEncoderR,GPIO.IN)
        GPIO.setup(self.PortEncoderH,GPIO.IN)
        GPIO.setup(self.TasteL,GPIO.IN)
        GPIO.setup(self.TasteR,GPIO.IN)
        GPIO.setup(self.portRoteTaste,GPIO.IN)

        GPIO.setup(self.PortLRueck,GPIO.OUT)
        GPIO.setup(self.PortRRueck,GPIO.OUT)

        #Motorern EIN/AUS
        #GPIO.output(self.PortRRueck,0)
        #GPIO.output(self.PortLRueck,0)
        
        print("Init Encoder")    

    def runAllTime(self):
        """Count pulse L und R und DistanzRad, loop"""
        EncoderLOld=GPIO.input(self.PortEncoderL)
        EncoderROld=GPIO.input(self.PortEncoderR)
        EncoderHOld=GPIO.input(self.PortEncoderH)
        self.CountL=0
        self.CountR=0
        self.CountH=0
  
        while True:
            
            if GPIO.input(self.PortEncoderL) != EncoderLOld:
                self.CountL +=1
                EncoderLOld= GPIO.input(self.PortEncoderL)
    
            if GPIO.input(self.PortEncoderR) != EncoderROld:
                self.CountR +=1
                EncoderROld= GPIO.input(self.PortEncoderR)
    
            if GPIO.input(self.PortEncoderH) != EncoderHOld:
                if GPIO.input(self.PortLRueck)and GPIO.input(self.PortRRueck)==1:
                    self.CountH -=1
                else:
                    self.CountH +=1                
                EncoderHOld= GPIO.input(self.PortEncoderH)
    
            self.DiffCount=self.CountR-self.CountL
            self.WegCount=self.CountH    
    
            ###Alarme### 
            if GPIO.input(self.TasteL)==1:
                self.AlarmL=True
                
            if GPIO.input(self.TasteR)==1:
                self.AlarmR=True

            sleep(0.05)

    def clearEncoderDist(self):
        """clears Dist-Counst"""
        self.WegCount=0
        self.CountH=0
        return
    
    def clearEncoderLR(self):
        """clears L / R Counts"""
        self.DiffCount=0
        self.CountR=0
        self.CountL=0
        return
    
    def getSteerDiff(self):
        """Abweichung zwischen L und R"""
        Ausgabe=self.DiffCount
        return(Ausgabe)

    def getDistCounts(self):
        """counts an Wegrad"""
        Ausgabe=self.WegCount
        self.WegCount=0
        return(Ausgabe)

    def getPumper(self):
        """TRUE,TRUE wenn Stossstange L/R gedrückt"""
        AlarmL=self.AlarmL
        AlarmR=self.AlarmR
        self.AlarmL=False
        self.AlarmR=False
        return (AlarmL,AlarmR)

    def getTaste(self):
        """Status der Roten Taste ausgeben"""
        return(GPIO.input(self.portRoteTaste))


if __name__ == "__main__":

    from threading import *
    print("Starte")
    Encoder=Encoder()
    ThreadEncoder=Thread(target=Encoder.runAllTime,args=())
    ThreadEncoder.daemon=True
    ThreadEncoder.start()

    while True:
        print(Encoder.getSteerDiff())
        sleep(1)


    
