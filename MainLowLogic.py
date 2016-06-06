#Robo Main

Robo=True

from Scanner import *
from Encoder import *
import Kompass
from Karte import *
from Plan import *
from Motor import *
from Grid import *
from Logic import *
import sys
import atexit

count=1
speed=0
steer=0
timer=0
encoder=Encoder()
navigation=Navigation()
scanner=Scanner()
karte=Karte(encoder)
plan=Plan()
kreis=0
motor=Motor()
grid=Grid(50,50)
logic=Logic()

grid.setZielInGrid(15,49)
grid.setStartInGrid(15,1)
karte.setRoboPosZero(150,150)

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
sleep(1)

while Robo==True:

    #get Distances from IR-Sensors
    dist_front, dist_left , dist_right, obstacles = scanner.getFixData()
    print(dist_front,dist_left, dist_right)

    #Obstacles eintragen
    karte.updateObstacles(obstacles)

    #Obstacles von Pumper eintragen
    pumperL,pumperR=encoder.getPumper()
    karte.updateHardObstacles(pumperL,pumperR)

    #Grid
    x,y,pose=karte.getRoboPos()
    grid.setStartInGrid(int(x/10),int(y/10))
    walls=karte.getObstacles()
    grid.obstaclesInGrid(walls)
    #grid.addClearance()
    grid.saveGridObstacles()
    
    #Position updaten
    deltaL,deltaR=encoder.getPulseLR()
    kompassCourse=Kompass.getKompass()
    karte.updateRoboPos(deltaL,deltaR,kompassCourse)
    karte.saveRoboPath()
    encoder.clearEncoderLR()


    #Plan next Steps
    logic.setRoboPos(x,y,pose)
    steer,speed=logic.wsa(dist_front,dist_left,dist_right,pumperL,pumperR)
    print(steer,speed)
    motor.setCommand(steer,speed)

    motor.booster(1,1)

    if encoder.getTaste() == 1:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sys.exit()
    print("************")
    sleep(1.2)


