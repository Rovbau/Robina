#!/usr/bin/env python
#-*- coding: utf-8 -*-


ScanList=[[-90,10],[-80,20],[-70,10],[-60,10],[-50,110],
          [-40,130],[10,140],[20,10],[30,10],[40,110],[50,110]]

from time import *
import RPi.GPIO as GPIO
from Sonar import *
import math
from threading import *
GPIO.setwarnings(False)
import smbus
bus = smbus.SMBus(1)



class Scanner():
    def __init__(self):
        """init Scanner und Servo"""
        setServoConfig()
        
        self.Sonar1=Sonar()

        self.lock=Lock()
        
        self.AusgabeList=[]
        self.RunScan=0
        self.ScanList=[]
        print("Init Scanner")

    def runAllTime(self,RunScan):
        """Scan runs all time"""

        self.ScanList=[]
        
        while RunScan==1:
            for angle in range(160, 0, -10):
                setServo(angle)
                sleep(0.2)
                Messwert,Error=self.Sonar1.GetADC()
                Messwert,Error=self.Sonar1.GetADC()
                
                self.lock.acquire()   
                self.ScanList.append([(90-angle),Messwert])
                self.lock.release()
            
            #self.ScanList=[]
            NewScanAvailable=1
                   
            for angle in range(10, 170, 10):
                setServo(angle)
                sleep(0.2)
                Messwert,Error=self.Sonar1.GetADC()
                Messwert,Error=self.Sonar1.GetADC()
                self.ScanList.append([(90-angle),Messwert])
                
            #ScanList.reverse()
            
            self.lock.acquire() 
            self.AusgabeList=ScanList[:]  #Deepcopy
            self.lock.release()
            
            #ScanList=[]
            NewScanAvailable=1             
        return()

    def getNewDistValues(self):
        Ausgabe=self.ScanList
        self.ScanList=[]
        return(Ausgabe)
    
        
#Funktionen für Servo intit
def setServoConfig():
    set("delayed", "0")
    set("mode", "servo")
    set("servo_max", "180")
    set("active", "1")

def set(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()	
    except:
        print("Error writing to: " + property + " value: " + value)

def setServo(angle):
    set("servo", str(angle))


if __name__ == "__main__":

    from threading import *
    print("Starte")
    Scanner1=Scanner()
    ThreadScanAllTime=Thread(target=Scanner1.runAllTime, args=(1,))
    ThreadScanAllTime.daemon=True
    ThreadScanAllTime.start()

    sleep(1)
    while True:
        print(Scanner1.getNewDistValues())
        sleep(0.6)
    


    
