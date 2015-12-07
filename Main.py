#Robo Main

Robo=True

from Scanner import *
from Encoder import *
from Kompass import *
from Karte import *
from Plan import *

karte=Karte()
navigation=Navigation()
scanner=Scanner()
plan=Plan(karte,navigation)
encoder=Encoder()
kompass=Kompass()


ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(1,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

while Robo==True:  
    obstacles=scanner.getNewDistValues()
    karte.updateObstacles(obstacles)
    #print(karte.getObstacles())

    deltaDist=encoder.getDistCounts()
    steerDiff=encoder.getSteerDiff()
    kompassCourse=kompass.getKompass()

    karte.updateRoboPos(deltaDist,steerDiff,kompassCourse)

    pumperL,pumperR=encoder.getPumper()
 #   Karte.updateHardObstacles(PumperL,PumperR)
    
    plan.getCourse()
## #   Motor.setCommand(Steer,Speed)

    sleep(1.5)

