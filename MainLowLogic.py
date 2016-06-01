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
timer=0
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

ThreadScanAllTime=Thread(target=scanner.runAllTime, args=(0,))
ThreadScanAllTime.daemon=True
ThreadScanAllTime.start()

ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()
sleep(1)

def turn(richtung, winkel):
    L,R=encoder.getPulseLR()
    
    if richtung == "right":
        motor.setCommand(-1,0)

        while L<winkel:
            speedL,speedR=encoder.getSpeedLR()
            motor.booster(speedL,0)

            L,R=encoder.getPulseLR()
            #sleep(0.1)
            
    if richtung == "left":
        motor.setCommand(1,0)

        while R<winkel:
            speedL,speedR=encoder.getSpeedLR()
            motor.booster(0,speedR)

            L,R=encoder.getPulseLR()
            #sleep(0.1)   


while Robo==True:

    dist_front, _ = scanner.Sonar1.GetADC()
    dist_left, _ = scanner.Sonar1.getScanDist("left")
    print(dist_front,dist_left)
    
    #Position updaten
    deltaL,deltaR=encoder.getPulseLR()
    kompassCourse=Kompass.getKompass()
    karte.updateRoboPos(deltaL,deltaR,kompassCourse)
    karte.saveRoboPath()
    encoder.clearEncoderLR()

    pumperL,pumperR=encoder.getPumper()
    if pumperL == True or pumperR == True:
        timer=10
    
    if dist_front<60:
        turn("right",2)
    elif dist_left<40:
        turn("right",2)
    elif dist_left>60 and dist_left<90:
        turn("left",2)        
    else:
        motor.setCommand(0,1)
        
    if pumperL == True or pumperR == True or timer>1:
        timer=timer-1
        motor.setCommand(0,-1)

        
##    
##    L,R=encoder.getPulseLR()
##    print(L,R)
##    if (R-L)>1:
##        motor.setCommand(-1,0)
##        print("Korr L")
##    if (L-R)>1:
##        motor.setCommand(1,0)
##        print("Korr R")
##    if abs(R-L)<1:
##        motor.setCommand(0,1)
##        print("Gerade")

    speedL,speedR=encoder.getSpeedLR()
    motor.booster(1,1)




    

    if encoder.getTaste() == 1:
        motor.setCommand(0,0)
        print("By By goto Sleep")
        sys.exit()
    print("************")
    sleep(0.2)


