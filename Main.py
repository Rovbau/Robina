#Robo Main


import Scanner

Scanner=Scanner()
Scanner.init()
Karte=Karte()
Karte.reset()
Plan=Plan()
Plan.clearAll()

ThreadScanner=Thread(target=Scanner.scanAllTime())
ThreadScanner.start()

ThreadEncoder=Thread(target=Encoder.runAllTime())
ThreadEncoder.start()

while Robo==True:  
    Obstacles=Scanner.getScanDiff()
    Karte.updateObstacles(Obstacles)

    DeltaDist=Encoder.getDistCounts()
    SteerDiff=Encoder.getSteerDiff()
    KompassCourse=Encoder.getKompass()

    Karte.updateRoboPos(DeltaDist,SteerDiff,KompassCourse)

    PumperL,PumperR=Encoder.pumper()
    Karte.updateHardObstacles(PumperL,PumperR)

    Plan.getCourse(Steer,Speed)
    Motor.setCommand(Steer,Speed)

