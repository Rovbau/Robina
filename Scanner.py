#!/usr/bin/env python
#-*- coding: utf-8 -*-
ScanList=[[-90,10],[-80,20],[-70,10],[-60,10],[-50,110],
          [-40,130],[10,140],[20,10],[30,10],[40,110],[50,110]]

from time import *
import RPi.GPIO as GPIO
from Sonar import *
from math import cos,sin,radians
from threading import *
GPIO.setwarnings(False)
import smbus
bus = smbus.SMBus(1)

class Scanner():
    def __init__(self):
        """init Scanner und Servo"""
        self.setServoConfig()
        self.Sonar1=Sonar()
        self.lock=Lock()
        self.RunScan=0
        self.ScanList=[]
        print("Init Scanner")

    def runAllTime(self,RunScan):
        """Scan runs all time"""
        self.ScanList=[]
        
        while RunScan==1:
            for angle in range(160, 0, -5):
                self.readSensorAndUpdateObstacles(angle)
            for angle in range(10, 170, 5):
                self.readSensorAndUpdateObstacles(angle)

    def readSensorAndUpdateObstacles(self,angle):
        self.setServo(angle)
        sleep(0.2)
        Messwert,Error=self.Sonar1.GetADC()
        Messwert,Error=self.Sonar1.GetADC()
        if Messwert<120:
            self.lock.acquire()
            self.ScanList.append([(angle-90),Messwert])
            self.lock.release()

    def getNewDistValues(self):
        Obstacles=self.ScanList
        Ausgabe=[]
        
        #Delta X/Y für Hindernis
        for i in range(len(Obstacles)):
            Dx=(Obstacles[i][1]*cos(radians(Obstacles[i][0])))
            Dy=(Obstacles[i][1]*sin(radians(Obstacles[i][0])))
            #print(int(Dx),int(Dy))
            Ausgabe.append((int(Dx),int(Dy)))
        self.ScanList=[]
        return(Ausgabe)

    def setServoConfig(self):
        self.setPwmPropertyset("delayed", "0")
        self.setPwmPropertyset("mode", "servo")
        self.setPwmPropertyset("servo_max", "180")
        self.setPwmPropertyset("active", "1")

    def setPwmPropertyset(self,prop, value):
        try:
            f = open("/sys/class/rpi-pwm/pwm0/" + prop, 'w')
            f.write(value)
            f.close()	
        except:
            print("Error writing to: " + prop + " value: " + value)

    def setServo(self,angle):
        self.setPwmPropertyset("servo", str(angle))
        
#Funktionen für Servo intit

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
