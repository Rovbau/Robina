# -*- coding: utf-8 -*-
#Encoder
#Programm fragt Radencoder L/R und DistGeber an Robo ab.
#Ausgabe von Distanz und Abweichung der Räder

from time import sleep , time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Encoder():
    def __init__(self):
        """init aller Ports, clears all counts"""
        self.PortEncoderL=32
        self.PortEncoderR=36
        self.PortEncoderH=7
        self.TasteL=13
        self.TasteR=15
        self.portRoteTaste=37

        self.PortLRueck=33
        self.PortRRueck=29

        self.WegCount=0
        self.DiffCount=0
        self.DistRad=0

        self.AlarmL=False
        self.AlarmR=False

        self.speedL=0
        self.speedR=0
        self.newSpeedL=0
        self.newSpeedR=0
        self.keypress_rot=0.00
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortEncoderL,GPIO.IN)
        GPIO.setup(self.PortEncoderR,GPIO.IN)
        GPIO.setup(self.PortEncoderH,GPIO.IN)
        GPIO.setup(self.TasteL,GPIO.IN)
        GPIO.setup(self.TasteR,GPIO.IN)
        GPIO.setup(self.portRoteTaste,GPIO.IN)

        GPIO.setup(self.PortLRueck,GPIO.OUT)
        GPIO.setup(self.PortRRueck,GPIO.OUT)
        #GPIO.setup(16,GPIO.OUT)
        #Motorern EIN/AUS
        GPIO.output(self.PortRRueck,0)
        GPIO.output(self.PortLRueck,0)
        
        print("Init Encoder")    

    def runAllTime(self):
        """Count pulse L und R und DistanzRad, loop"""
        EncoderLOld=GPIO.input(self.PortEncoderL)
        EncoderROld=GPIO.input(self.PortEncoderR)
        EncoderHOld=GPIO.input(self.PortEncoderH)
        self.CountL=0
        self.CountR=0
        self.CountH=0
        self.DistRad=0
        start_t = 5473278887

        while True:
            #GPIO.output(16,1)            
            if GPIO.input(self.PortEncoderL) != EncoderLOld:
                self.newSpeedL=time()
                
                if GPIO.input(self.PortLRueck)==1:
                    self.CountL -=1
                else:
                    self.CountL +=1
                EncoderLOld= GPIO.input(self.PortEncoderL)
    
            if GPIO.input(self.PortEncoderR) != EncoderROld:
                self.newSpeedR=time()
                
                if GPIO.input(self.PortRRueck)==1:
                    self.CountR -=1
                else:
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
            
            ###Booster###
            self.speedL=time()-self.newSpeedL
            self.speedR=time()-self.newSpeedR
    
            ###Alarme### 
            if GPIO.input(self.TasteL)==1:
                self.AlarmL=True
                
            if GPIO.input(self.TasteR)==1:
                self.AlarmR=True

            ###RoteTaste###
            if GPIO.input(self.portRoteTaste)==1:
                self.keypress_rot += 1.00
            else:
                self.keypress_rot = 0.00
            #GPIO.output(16,0)
            sleep(0.01)

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
    
    def getSpeedLR(self):
        return(self.speedL,self.speedR)
    
    def getPulseLR(self):
        """Pulse an  L und R Rad"""
        return(self.CountL,self.CountR)

    def getDistCounts(self):
        """counts an Wegrad hinten"""
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

    def getTastenPress(self):
        """Time Sec. Keypress der Roten Taste ausgeben"""
        return(float(self.keypress_rot/50))


if __name__ == "__main__":

    from threading import *
    print("Starte")
    Encoder=Encoder()
    ThreadEncoder=Thread(target=Encoder.runAllTime,args=())
    ThreadEncoder.daemon=True
    ThreadEncoder.start()

    sleep(0.3)
    while True:
        print(Encoder.getPulseLR())
        print(Encoder.getSpeedLR())
        sleep(5)


    
