#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Programm steuert zwei Motoren an Robo



from time import *
import RPi.GPIO as GPIO
from Encoder import *
from Karte import *

GPIO.setwarnings(False)

class Motor():
    def __init__(self):
        self.PortLVor=35
        self.PortLRueck=29
        self.PortRVor=31
        self.PortRRueck=33

        self.steerOld=0
        self.speedOld=0

        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.PortLVor,GPIO.OUT)
        GPIO.output(self.PortLVor,0)
        
        GPIO.setup(self.PortLRueck,GPIO.OUT)
        GPIO.output(self.PortLRueck,0)
        
        GPIO.setup(self.PortRVor,GPIO.OUT)
        GPIO.output(self.PortRVor,0)
        
        GPIO.setup(self.PortRRueck,GPIO.OUT)
        GPIO.output(self.PortRRueck,0)
        
        print("Init Motoren")
    
    def setCommand(self,steer,speed):
        """Setze Motor Commands Steer= -1,0-1 (L/R/0) and Speed -1,0,1 (Vor/Ret/0)"""

        #Stromspitzen verhindern warte 100ms
        if steer != self.steerOld or speed != self.speedOld:
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,0)
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,0)
            self.steerOld=steer
            self.speedOld=speed
            sleep(0.1)
        
        if steer == 0 and speed == 1:        
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,0)
            GPIO.output(self.PortRVor,1)
            GPIO.output(self.PortLVor,1)
        elif steer == 0 and speed == 0:
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,0)            
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,0)
        elif steer == 0 and speed == -1:
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,0)            
            GPIO.output(self.PortLRueck,1)
            GPIO.output(self.PortRRueck,1)
        elif steer == 1 and speed >= 0:
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,1)            
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,0)
        elif steer == -1 and speed >= 0:
            GPIO.output(self.PortRVor,1)
            GPIO.output(self.PortLVor,0)            
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,0)
        elif steer == 1 and speed == -1:
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,0)            
            GPIO.output(self.PortLRueck,0)
            GPIO.output(self.PortRRueck,1)
        elif steer == -1 and speed == -1:
            GPIO.output(self.PortRVor,0)
            GPIO.output(self.PortLVor,0)            
            GPIO.output(self.PortLRueck,1)
            GPIO.output(self.PortRRueck,0)
        else:
            return(False)

        return(steer,speed)
        

if __name__ == "__main__":

    m=Motor()
    sleep(2)
    x=m.setCommand(-1,0)
    print(x)
    sleep(2)
    x=m.setCommand(1,0)
    print(x)
    sleep(2)
    x=m.setCommand(0,-1)
    print(x)
    sleep(2)
    x=m.setCommand(0,0)
    print(x)








                
        
