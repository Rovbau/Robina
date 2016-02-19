#Robo Main

Robo=True

from Scanner import *
from Encoder import *
import Kompass
from Karte import *
from Plan import *
from Motor import *
from Grid import *
import sys
import atexit

count=1
speed=0
steer=0
encoder=Encoder()
navigation=Navigation()
scanner=Scanner()
karte=Karte(encoder)
plan=Plan()
kreis=0
motor=Motor()
grid=Grid(50,50)

grid.setZielInGrid(15,49)
grid.setStartInGrid(15,1)
karte.setRoboPosZero(150,150)

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
sleep(1)

while Robo==True:
    #Obstacles eintragen
    obstacles=scanner.getNewDistValues()
    #obstacles=[[0,50],[10,50],[20,50],[30,50],[40,50],[50,50]]
    karte.updateObstacles(obstacles)
    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)
    
    #Position updaten
    deltaL,deltaR=encoder.getPulseLR()
    kompassCourse=Kompass.getKompass()
    karte.updateRoboPos(deltaL,deltaR,kompassCourse)
    karte.saveRoboPath()
    
    #Grid mit Astar
    x,y,pose=karte.getRoboPos()
    grid.setStartInGrid(int(x/10),int(y/10))
    walls=karte.getObstacles()
    grid.obstaclesInGrid(walls)
    grid.addClearance()
    grid.saveGridObstacles()

    #motor.setCommand(0,0)
    path=grid.getSolvedPath(motor)

    grid.saveGridPath(path)
    #print("Path:"+str(path))
    

    steer,speed=plan.nextStep(path,x,y,pose)
    wall_near=grid.obstacleNear()
    steer,speed=plan.ZuNahe(steer,speed,wall_near)

    
    #motor.setCommand(0,0)


    count += 1
    if count < 1:
        speed=0
        steer=0
        count=0
        motor.setCommand(steer,speed)
        print(karte.getRoboPos())
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

    if encoder.getTaste() == 1:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sys.exit()
    print("************")
    sleep(0.2)


