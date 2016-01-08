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

encoder=Encoder()
navigation=Navigation()
scanner=Scanner()
karte=Karte(encoder)
plan=Plan(karte,navigation)
motor=Motor()

def cleaning():
    """Do cleanup at end, command are visVersa"""
    motor.setCommand(0,0)

atexit.register(cleaning)

ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(1,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

while Robo==True:
    print("***************************************")  
    obstacles=scanner.getNewDistValues()
    karte.updateObstacles(obstacles)

    deltaDist=encoder.getDistCounts()
    steerDiff=encoder.getSteerDiff()
    kompassCourse=Kompass.getKompass()

    karte.updateRoboPos(deltaDist,steerDiff,kompassCourse)

    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)

    steer,speed=plan.getCourse()
    print("Motor Command:" +str(steer))
    #sleep(2)
    motor.setCommand(steer,speed)
    #sleep(0.2)
    #motor.setCommand(0,0)
    if encoder.getTaste() == 1:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sys.exit()

    sleep(0.15)


