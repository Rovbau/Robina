#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import time

class Servo():
    def __init__(self):
        os.system("gpio -g mode 18 pwm")
        os.system("gpio pwm-ms")
        os.system("gpio pwmc 192")
        os.system("gpio pwmr 2000")
        os.system("gpio -g pwm 18 130")  #Set to Middle

    def set_servo(self, angle):
        ms_sec = angle + 130 
        os.system("gpio -g pwm 18 " +str(ms_sec))
        
        
if __name__ == "__main__":

    servo = Servo()
    
    for i in range(-90,100,10):
        servo.set_servo(i)
        print(i)
        time.sleep(0.5)
