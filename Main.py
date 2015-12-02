#Robo Main


import Scanner
import Encoder
import Kompass


Scanner=Scanner()
Karte=Karte()
Plan=Plan()


ThreadScanAllTime=Thread(target=Scanner1.runAllTime, args=(1,))
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
    Karte.updateHardObstacles(PumperL,PumperR)

    Plan.getCourse(Steer,Speed)
    Motor.setCommand(Steer,Speed)

