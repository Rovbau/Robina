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
    def __init__(self):
        """init Weggeber IC """
        self.PortLRueck=33
        self.PortRRueck=29

        self.DiffCount = 0
        self.counts_left_old = 0
        self.counts_right_old = 0
        self.CountL = 0
        self.CountR = 0
       
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PortLRueck,GPIO.OUT)
        GPIO.setup(self.PortRRueck,GPIO.OUT)

        #Set PLC-IC to counter mode
        self.addrweggeberL=0x51
        self.addrweggeberR=0x50
        
        bus.write_byte_data(self.addrweggeberL,0x00,0x20)           #PLC8583, Adress ,Register 0x00, Commando=Countermode 0x20
        bus.write_byte_data(self.addrweggeberL,0x01,0x00)           #Counter Register 1+2 clear
        bus.write_byte_data(self.addrweggeberL,0x02,0x00)
        
        bus.write_byte_data(self.addrweggeberR,0x00,0x20)           #PLC8583, Adress ,Register 0x00, Commando=Countermode 0x20
        bus.write_byte_data(self.addrweggeberR,0x01,0x00)           #Counter Register 1+2 clear
        bus.write_byte_data(self.addrweggeberR,0x02,0x00)
        
        print("Init Weggeber")    

    def runAllTime(self):
        """Count pulse L und R und DistanzRad, loop"""

        #Get Weggeber counts and clear Register
        left = bus.read_word_data(self.addrweggeberL,0x01)
        countsL = int(hex(left).replace('0x', ''))          #BCD-Code to Int
        
        right = bus.read_word_data(self.addrweggeberR,0x01)        
        countsR = int(hex(right).replace('0x', ''))         #BCD-Code to Int

        aktualL_counts = countsL - self.counts_left_old 
        aktualR_counts = countsR - self.counts_right_old

        self.counts_left_old = countsL
        self.counts_right_old = countsR
        
        if countsL > 900 or countsR > 900:
            bus.write_word_data(self.addrweggeberL,0x01,0x00)       
            bus.write_word_data(self.addrweggeberR,0x01,0x00)            

            self.counts_left_old = 0
            self.counts_right_old = 0


        #Count minus wenn Robo retour                       
        if GPIO.input(self.PortLRueck)==1 or GPIO.input(self.PortRRueck)==1:
            self.CountL = self.CountL + aktualL_counts * (-1)
            self.CountR = self.CountR + aktualR_counts * (-1)
        else:
            self.CountL = self.CountL + aktualL_counts
            self.CountR = self.CountR + aktualR_counts
        
        #if GPIO.input(self.PortRRueck)==1:
        #    self.CountR = self.CountR + aktualR_counts * (-1)
        #else:
        #    self.CountR = self.CountR + aktualR_counts

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




if __name__ == "__main__":

    from threading import *
    print("Starte")
    weggeber=Weggeber()

    while True:
        weggeber.runAllTime()
        print(weggeber.getPulseLR())
        sleep(0.21)


    
