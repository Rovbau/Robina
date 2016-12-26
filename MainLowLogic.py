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
from ManuellKey import *
from SendJson import *
from Weggeber import *
import sys
import atexit
import os
import profile


count=1
speed=0
steer=0
timer=0
deltaL=0
deltaR=0
encoder=Encoder()
navigation=Navigation()
scanner=Scanner()
karte=Karte(encoder)
plan=Plan()
kreis=0
motor=Motor()
grid=Grid(50,50)
logic=Logic()
manuell=Manuell()
json=Json()
weggeber=Weggeber()

grid.setZielInGrid(20,10)
grid.setStartInGrid(1,1)
karte.setRoboPosZero(0,0)
plan.setGlobalZiel(2000,0)

def cleaning():
    """Do cleanup at end, command are visVersa"""
    motor.setCommand(0,0)
atexit.register(cleaning)

#SCAN OFF 
ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(0,))
ThreadScanAllTime.daemon=True
#ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

ThreadEncoder=Thread(target=manuell.runManuell,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()

##ThreadEncoder=Thread(target=weggeber.runAllTime,args=())
##ThreadEncoder.daemon=True
##ThreadEncoder.start()
    
sleep(1)


while Robo==True:
    os.system("clear")

    #get Distances from IR-Sensors
    dist_front, dist_left , dist_right, obstacles = scanner.getFixData()
    print(dist_front,dist_left, dist_right)

    #Obstacles eintragen
    karte.updateObstacles(obstacles)

    #Obstacles von Pumper eintragen
    pumperL,pumperR=encoder.getPumper()
    deltaH = encoder.getDistCounts()
    pumperL, pumperR  = logic.blocked(steer,speed,deltaH, pumperL, pumperR)

    karte.updateHardObstacles(pumperL,pumperR)

    #Grid
    x,y,pose=karte.getRoboPos()
    #print("Pose:"+str(int(pose)))
    grid.setStartInGrid(int(x/10),int(y/10))
    walls=karte.getObstacles()

    grid.obstaclesInGrid(walls)
    #grid.addClearance()
    grid.saveGridObstacles()

    #solved_path = grid.getSolvedPath(steer,speed,motor)
   
    #Position updaten
    weggeber.runAllTime()
    deltaL,deltaR=weggeber.getPulseLR()
    #print(deltaL,deltaR)
    kompassCourse=Kompass.getKompass()
    karte.updateRoboPos(deltaL,deltaR,kompassCourse)
    karte.saveRoboPath()
    encoder.clearEncoderLR()
    encoder.clearEncoderDist()
    weggeber.clearWeggeberLR()
    #Send Data via NET
    solved_path = []
    roundet_walls=grid.getRoundetWalls()
    #print(roundet_walls)
    #json.sendVisual(roundet_walls, [[x,y]],solved_path)
    
    #Ziel erreicht?
    logic.setRoboPos(x,y,pose)
    kurs_to_ziel,dist_to_ziel=plan.calcGlobalZielkurs(x,y,pose)
    print("KursZuZiel: "+str(kurs_to_ziel))
    print("DistZuZiel: "+str(dist_to_ziel))
    logic.setZielkurs(kurs_to_ziel)
    plan.zielErreicht(dist_to_ziel,motor)
    
    #Plan next Steps    
    steer,speed=logic.wsa(dist_front,dist_left,dist_right,pumperL,pumperR)
    steer,speed=logic.checkPumperStatus(pumperL,pumperR,steer,speed)
    print(steer,speed)
    speed_L,speed_R = encoder.getSpeedLR()
    motor.booster(speed_L,speed_R)
    #sleep(0.3)
    #motor.setCommand(0,0)

    #Manuell Control
    #steer,speed=manuell.getManuellCommand()
    motor.setCommand(steer,speed)
    print(karte.getRoboPos())
    #sleep(0.3)
    #motor.setCommand(0,0)

    if encoder.getTastenPress() > 0.1:
        motor.setCommand(0,0)
        sleep(5)
            
    if encoder.getTastenPress() > 2:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sleep(4)
        if encoder.getTastenPress() > 6:
            os.system("sudo shutdown -h 1")
            sys.exit()
        else:
            sys.exit()

    Spann, _ = scanner.Sonar1.GetBatSpann()
    if Spann < 7:
        print("ACHTUNG BATTERIE LEER")

    
    print("************")
    sleep(0.4)


