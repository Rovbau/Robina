#!/usr/bin/env python
#-*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
#GPIO.setwarnings(False)

import smbus
from time import *
bus = smbus.SMBus(1)



def getKompass():
    """Returns KompassKurs"""
    Kurs=0
    KompassAdress=0x61
    daten1=bus.read_byte_data(KompassAdress,0x02)
    daten2=bus.read_byte_data(KompassAdress,0x03)

    Kurs=(daten1<<8)+daten2
    Kurs=Kurs/10
    Kurs= 360 - Kurs
    return(Kurs)

if __name__ == "__main__":

    while True:
        print("Starte")
        print(getKompass())
        sleep(1)
