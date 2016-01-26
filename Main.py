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
plan=Plan(karte,navigation)
kreis=0
motor=Motor()
grid=Grid(30,30)

grid.setZielInGrid(25,25)
grid.setStartInGrid(10,3)

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
    #obstacles=[[50,0],[50,50],[0,50]]
    karte.updateObstacles(obstacles)
    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)
    
    #Position updaten
    deltaL,deltaR=encoder.getPulseLR()
    kompassCourse=Kompass.getKompass()
    karte.updateRoboPos(deltaL,deltaR,kompassCourse)
    karte.saveRoboPath()
    
    #Grid mit Astar
    walls=karte.getObstacles()
    grid.obstaclesInGrid(walls)
    #grid.addClearance()
    grid.saveGridObstacles()
    #x,y,pose=karte.getRoboPos()
    path=grid.getSolvedPath()
    grid.saveGridPath(path)

    count += 1
    if count == 10:
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

    sleep(0.2)


