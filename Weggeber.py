# -*- coding: utf-8 -*-
#Weggeber
#Programm fragt Radencoder per I2c ab L/R.
#Ausgabe von Distanz und Abweichung der Räder

from time import sleep , time
import RPi.GPIO as GPIO
import smbus
bus = smbus.SMBus(1)
GPIO.setwarnings(False)

class Weggeber():
    def __init__(self, motor_pwm):
        """init Weggeber IC """
        self.PortLRueck=33
        self.PortRRueck=29

        self.DiffCount = 0
        self.counts_left_old = 0
        self.counts_right_old = 0
        self.CountL = 0
        self.CountR = 0
        self.last_time = 0
        self.motor_pwm = motor_pwm
       
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortLRueck,GPIO.OUT)
        GPIO.setup(self.PortRRueck,GPIO.OUT)

        #PIC Adresse
        self.addrweggeber=0x18
        _ = bus.read_byte_data(self.addrweggeber,0x01)  #Dummy read damit Counter null
        _ = bus.read_byte_data(self.addrweggeber,0x03)

        print("Init Weggeber")    

    def runAllTime(self):
        """Count pulse L und R und DistanzRad, loop"""

        #Get Weggeber counts and clear Register
        left_low = bus.read_byte_data(self.addrweggeber,0x01)  #Read PIC Register1 => CountsLowByte
        left_high = bus.read_byte_data(self.addrweggeber,0x02)  #read CountsHighByte
        left = (left_high << 8) + left_low
        if left > 32767:
            left = (65536 - left) * (-1)
        self.CountL = left
       
        right_low = bus.read_byte_data(self.addrweggeber,0x03)  #Read PIC Register1 => CountsLowByte
        right_high = bus.read_byte_data(self.addrweggeber,0x04)  #read CountsHighByte
        right = (right_high << 8) + right_low
        if right > 32767:
            right = (65536 - right) * (-1)
        self.CountR = right        
        
        self.DiffCount=self.CountR-self.CountL
        return
    
    def clearWeggeberLR(self):
        """clears L / R Counts"""
        self.DiffCount=0
        self.CountR=0
        self.CountL=0
        return
    
    def getPulseLR(self):
        """Pulse an  L und R Rad"""
        return(self.CountL,self.CountR)

    def getSpeedLR(self):
        """Anzahl Pulse je Sec"""
        diff = time() - self.last_time
        self.last_time = time()
        speedL = 1/diff * self.CountL
        speedR = 1/diff * self.CountR
        return(speedL, speedR)

if __name__ == "__main__":

    from threading import *
    print("Starte")

    class Psydo():
        def __init__(self):
            pass
        def motor_is_backward(self):
            return(False)

    p = Psydo()
    weggeber=Weggeber(p)

    while True:
        weggeber.runAllTime()
        print(weggeber.getPulseLR())
        print(weggeber.getSpeedLR())
        sleep(0.21)


    
