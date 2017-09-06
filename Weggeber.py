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
        _ = bus.read_byte_data(self.addrweggeber,0x02)

        print("Init Weggeber")    

    def runAllTime(self):
        """Count pulse L und R und DistanzRad, loop"""

        #Get Weggeber counts and clear Register
        left = bus.read_byte_data(self.addrweggeber,0x01)  #Read PIC Register1 => CountsL
        if left > 127:
            left = (256-left) * (-1)
        self.CountL = left
        assert left < 100 , "Counter left Overrun"
        
        right = bus.read_byte_data(self.addrweggeber,0x02)  #Read PIC Register2 => CountsR
        if right > 127:
            right = (256-right) * (-1)
        self.CountR  = right
        assert right < 100 , "Counter right Overrun"
        
##        aktualL_counts = countsL - self.counts_left_old 
##        aktualR_counts = countsR - self.counts_right_old
##
##        self.counts_left_old = countsL
##        self.counts_right_old = countsR
##        
##        if countsL > 900 or countsR > 900:
##            bus.write_word_data(self.addrweggeberL,0x01,0x00)       
##            bus.write_word_data(self.addrweggeberR,0x01,0x00)            
##
##            self.counts_left_old = 0
##            self.counts_right_old = 0


##        #Count minus wenn Robo retour
##        if self.motor_pwm.motor_is_backward()== True :
##            self.CountL = self.CountL + aktualL_counts * (-1)
##            self.CountR = self.CountR + aktualR_counts * (-1)
##        else:
##            self.CountL = self.CountL + aktualL_counts
##            self.CountR = self.CountR + aktualR_counts
##        
##        #if GPIO.input(self.PortRRueck)==1:
##        #    self.CountR = self.CountR + aktualR_counts * (-1)
##        #else:
##        #    self.CountR = self.CountR + aktualR_counts

        self.DiffCount=self.CountR-self.CountL

    
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
#        print(weggeber.getSpeedLR())
        sleep(0.21)


    
