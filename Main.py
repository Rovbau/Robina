#Robo Main

Robo=True

from Scanner import *
from Encoder import *
import Kompass
from Karte import *
from Plan import *
from Motor import *
import sys
import atexit

count=1
speed=0
steer=0
encoder=Encoder()
navigation=Navigation()
scanner=Scanner()
karte=Karte(encoder)
plan=Plan(karte,navigation)
kreis=0
motor=Motor()

def cleaning():
    """Do cleanup at end, command are visVersa"""
    motor.setCommand(0,0)

atexit.register(cleaning)

ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(0,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()
sleep(0.2)

while Robo==True:
    #print("***************************************")  
    obstacles=scanner.getNewDistValues()
    karte.updateObstacles(obstacles)

    deltaL,deltaR=encoder.getPulseLR()

    kompassCourse=Kompass.getKompass()

    karte.updateRoboPos(deltaL,deltaR,kompassCourse)

    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)
    #print(Kompass.getKompass())
    count += 1
    if count == 10:
        speed=0
        steer=0
        count=0
        motor.setCommand(steer,speed)
        print(karte.getRoboPos())
        print(kreis)        #karte.setRoboPosZero()
        comm=input("COMMAND PLEASE: ")
        if comm == 8:
            speed=1
            steer=0
        elif comm == 6:
            speed=0
            steer=1
        elif comm == 4:
            speed=0
            steer=-1
        elif comm == 0:
            speed=0
            steer=0

        
        

    #steer,speed=plan.getCourse()
    #print("Motor Command:" +str(steer))

    motor.setCommand(steer,speed)
    #sleep(0.2)
    #motor.setCommand(0,0)
    if encoder.getTaste() == 1:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sys.exit()

    sleep(0.15)


