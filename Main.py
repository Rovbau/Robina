#Robo Main

Robo=True

from Scanner import *
from Encoder import *
import Kompass
from Karte import *
from Plan import *
from Motor import *

karte=Karte()
navigation=Navigation()
scanner=Scanner()
plan=Plan(karte,navigation)
encoder=Encoder()
motor=Motor()



ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(1,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

while Robo==True:  
    obstacles=scanner.getNewDistValues()
    karte.updateObstacles(obstacles)

    deltaDist=encoder.getDistCounts()
    steerDiff=encoder.getSteerDiff()
    kompassCourse=Kompass.getKompass()

    karte.updateRoboPos(deltaDist,steerDiff,kompassCourse)

    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)
    
    steer,speed=plan.getCourse()
    print(steer,speed)
    motor.setCommand(steer,speed)

    sleep(1.5)

