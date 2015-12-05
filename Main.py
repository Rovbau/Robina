#Robo Main

Robo=True

from Scanner import *
from Encoder import *
from Kompass import *
from Karte import *
from Plan import *


Scanner=Scanner()
Karte=Karte()
Plan=Plan()
Encoder=Encoder()
Kompass=Kompass()
Navigation=Navigation()

ThreadScanAllTime=Thread(target=Scanner.runAllTime, args=(1,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=Encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

while Robo==True:  
    Obstacles=Scanner.getNewDistValues()
    Karte.updateObstacles(Obstacles)

    DeltaDist=Encoder.getDistCounts()
    SteerDiff=Encoder.getSteerDiff()
    KompassCourse=Kompass.getKompass()

    Karte.updateRoboPos(DeltaDist,SteerDiff,KompassCourse)

    PumperL,PumperR=Encoder.getPumper()
 #   Karte.updateHardObstacles(PumperL,PumperR)
    

    Plan.getCourse()
 #   Motor.setCommand(Steer,Speed)

