#!/usr/bin/env python
#-*- coding: utf-8 -*-
ScanList=[[-90,10],[-80,20],[-70,10],[-60,10],[-50,110],
          [-40,130],[10,140],[20,10],[30,10],[40,110],[50,110]]

from time import *
import RPi.GPIO as GPIO
from Sonar import *
from math import cos,sin,radians
from threading import *
from Lidar import *
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
        self.setServo(90)
	self.lidar = Lidar_Lite()
	self.lidar.connect(1)
        print("Init Scanner")

    def runAllTime(self,RunScan):
        """Scan runs all time"""
        self.ScanList=[]
        
        while RunScan==1:
            for angle in range(160, 0, -1):
                self.readSensorAndUpdateObstacles(angle)
            for angle in range(10, 170, 1):
                self.readSensorAndUpdateObstacles(angle)

    def readSensorAndUpdateObstacles(self,angle):
        self.setServo(angle)
        sleep(0.5)
        #Messwert,Error=self.Sonar1.GetADC(0)
        #Messwert,Error=self.Sonar1.GetADC(0)
        Messwert = self.lidar.getDistance()
        self.ScanList.append([(angle-90),Messwert])
           

    def getNewDistValues(self):
        Obstacles=self.ScanList
        Ausgabe=[]        
        #Delta X/Y für Hindernis
        for i in range(len(Obstacles)):
            Dx=(Obstacles[i][1]*cos(radians(Obstacles[i][0])))
            Dy=(Obstacles[i][1]*sin(radians(Obstacles[i][0])))
            Ausgabe.append([int(Dx),int(Dy)])
        self.ScanList=[]
        return(Ausgabe)


    def getFixData(self):
        """Lese 3 Sensorwerte und returns Dist"""
        dist_list=[]

        front,_ = self.Sonar1.GetADC(0)
        if front < 90:
            dx,dy = self.distInPolar(front,0)
            dist_list.append([dx,dy])
        
        left,_ = self.Sonar1.GetADC(2)
        if left < 90:
            dx,dy = self.distInPolar(left,65)
            dist_list.append([dx,dy+10])
            
        right,_ = self.Sonar1.GetADC(3)
        if right < 90:
            dx,dy = self.distInPolar(right,-65)
            dist_list.append([dx,dy-10])
            
        return(front,left,right,dist_list)
           
    def distInPolar(self,dist,winkel):
        """returns aus Dist und Winkel Dx,Dy ab RoboPosition"""
        
        Dx=int((dist*cos(radians(winkel))))
        Dy=int((dist*sin(radians(winkel))))
        return(Dx,Dy)

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
        #print(Scanner1.getFixData())
        sleep(1)
