#!/usr/bin/env python
#-*- coding: utf-8 -*-

from time import *
from math import cos,sin,radians
from threading import *
from Lidar import *
from Servo import *
from Sonar import *
import smbus
bus = smbus.SMBus(1)

class Scanner():
    def __init__(self):
        """init Scanner und Servo"""
        self.sonar1 = Sonar()
        self.run_scan = 0
        self.scan_list= []
        self.servo = Servo()
        self.servo_step = 10
	self.lidar = Lidar_Lite()
	self.lidar.connect(1)
        print("Init Scanner, Servo")

    def runAllTime(self,run_scan):
        """Servo Scan from -90 to 90 Grad"""
        self.run_scan = run_scan
        self.scan_list=[]
        
        while self.run_scan == 1:
            for angle in range(-90, 100, self.servo_step):
                self.readSensorAndUpdateObstacles(angle)
            for angle in range(85, -95 , self.servo_step*(-1)):
                self.readSensorAndUpdateObstacles(angle)

    def readSensorAndUpdateObstacles(self,angle):
        """Set Servo angle, get Distance[cm] from Lidar append to scan_list"""
        self.servo.set_servo(angle)
        print(angle)
        sleep(0.20)
        messwert = self.lidar.getDistance()
        if messwert < 900:
            self.scan_list.append([angle, messwert])
           

    def getNewDistValues(self):
        """Returns obstacle list with dx/dy[cm] in local grid""" 
        obstacles=self.scan_list
        ausgabe=[]        
        #Delta X/Y für Hindernis
        for i in range(len(obstacles)):
            Dx=(obstacles[i][1]*cos(radians(obstacles[i][0])))
            Dy=(obstacles[i][1]*sin(radians(obstacles[i][0])))
            ausgabe.append([int(Dx),int(Dy)])
        self.scan_list=[]
        return(ausgabe)

    def getFixData(self):
        """Returns 3 IR-Sensorwerte and list with dx/dy[cm] in local grid"""
        dist_list=[]

        front,_ = self.sonar1.GetADC(0)
        if front < 90:
            dx,dy = self.distInPolar(front,0)
            dist_list.append([dx,dy])
        
        left,_ = self.sonar1.GetADC(2)
        if left < 90:
            dx,dy = self.distInPolar(left,65)
            dist_list.append([dx,dy+10])
            
        right,_ = self.sonar1.GetADC(3)
        if right < 90:
            dx,dy = self.distInPolar(right,-65)
            dist_list.append([dx,dy-10])
            
        return(front,left,right,dist_list)
           
    def distInPolar(self,dist,winkel):
        """returns aus Dist und Winkel, dx/dy ab RoboPosition"""       
        Dx=int((dist*cos(radians(winkel))))
        Dy=int((dist*sin(radians(winkel))))
        return(Dx,Dy)

if __name__ == "__main__":

    from threading import *
    print("Starte")
    scanner1=Scanner()
    ThreadScanAllTime=Thread(target=scanner1.runAllTime, args=(1,))
    ThreadScanAllTime.daemon=True
    ThreadScanAllTime.start()

    sleep(1)
    while True:
        print(scanner1.getNewDistValues())
        #print("Fix Data from IR: ")
        #print(scanner1.getFixData())
        sleep(1)
