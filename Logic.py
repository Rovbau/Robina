#Logic

import time
import math


class Logic():
    def __init__(self):
        """init Logic objekt"""
        self.timer=0
        self.steer=0
        self.speed=0
        self.flag_leftWall=False
        self.flag_rightWall=False
        self.zielkurs=0
        self.x=0
        self.y=0
        self.oldx=0
        self.oldy=0
        self.pose=50
        self.generatorL = self.ret_flow_L()
        self.generatorR = self.ret_flow_R()
        self.generatorLR = self.ret_flow_LR()
        self.command=[]
        self.retour_done = True
        
        print("Init Logic")
            
    def wsa(self,dist_front,dist_left,dist_right,pumperL,pumperR):
        """Wandering Standpoint Algorithm"""
        print("WSA")
        self.dist_front=dist_front
        self.dist_left=dist_left
        self.dist_right=dist_right

        #Wall-Mode oder GeradeFahrt
        if self.dist_front > 60 and self.flag_leftWall == False and self.flag_rightWall == False:
            self.turnToGoal()
            self.speed=1
        else:
            self.wallMode()
            
        return(self.steer,self.speed)

    def turnToGoal(self):
        """Wenn kein Obstacle nahe, Drehe zu Zielkurs"""

        print("GOAL")
        winkel=self.getKursDiff(self.zielkurs,self.pose)
        
        if winkel > 10:
            self.steer=1
        elif winkel < -10:
            self.steer=-1
        else:
            self.steer=0
        
    def wallMode(self):
        """Wall-Modus Robo folgt Links oder Recht"""
        print("WALL")

        #Deside Wall L oder R
        if self.getKursDiff(self.zielkurs,self.pose) >= 0:
            self.flag_leftWall = True
            aktiv_sensorLR = self.dist_left
        else:
            self.flag_rightWall = True
            aktiv_sensorLR = self.dist_right
            
        winkel=self.getKursDiff(self.zielkurs,self.pose)
        
        if self.dist_front < 70:
            self.steer = -1
            
        if aktiv_sensorLR < 30:
            self.steer = -1
            
        if self.dist_front > 70 and aktiv_sensorLR > 40:
            self.steer = 1

        if aktiv_sensorLR > 30 and aktiv_sensorLR < 40:
            self.steer = 0
            
        if abs(winkel)< 10 and self.dist_front > 70 and aktiv_sensorLR > 70:
            self.flag_leftWall = False
            self.flag_rightWall = False
            self.steer = 0
            
        #Invert Kurvenkommando wenn Right Wall
        if self.flag_rightWall == True:
            self.steer = self.steer * (-1)
            
        print(self.flag_leftWall,self.flag_rightWall)
        
    def getKursDiff(self,soll,ist):
        """Diff zwischen zwei Winkel 0-360grad"""

        if soll>ist:
            if soll-ist>180:
                Winkel=(abs(ist-soll)-360)
            else:
                Winkel=soll-ist
        else:     
            if ist-soll>180:
                Winkel=360-(ist-soll)
            else:
                Winkel=soll-ist
        print("Winkel: "+str(Winkel))
        return(Winkel)

    def getCommand(self):
        """Return Kurs Empfehlung (steer,speed) von WSA-Algorithm"""
        return(self.steer,self.speed)

    def setRoboPos(self,x,y,pose):
        """Set Robo position (GlobX, GlobY, GlobPose) for WSA-Algorithm"""
        self.x = x
        self.y = y
        self.pose = pose


        
    def ret_flow_L(self):
        """Ablauf fuer Retour wenn PumperL"""
        yield ([0,-1,50])
        yield([-1,-1,25])
        yield (0,-1,20)
        yield (999,0,0)

    def ret_flow_R(self):
        """Ablauf fuer Retour wenn PumperR"""
        yield (0,-1,50])
        yield([1,-1,25])
        yield (0,-1,20)
        yield (999,0,0)

    def ret_flow_LR(self):
        """Ablauf fuer Retour wenn Pumper L+R"""
        yield ([0,-1,50])
        yield([0,-1,50])
        yield (0,-1,40)
        yield (999,0,0)

        
    def checkDistDrive(self,dist,t):
        """returns True if RetourDistance (dist) is Done"""

        actual_dist= math.sqrt(pow(self.x-self.oldx,2)+pow(self.y-self.oldy,2))

        print(actual_dist)
        drive_time= time.time() - self.t
        
        if abs(actual_dist) > dist or drive_time > 4:
            dist_done=True
        else:
            dist_done=False
            
        return(dist_done)

    def pumperUmfahren(self,steer,speed):
        """Umfahre HardObstacle"""

        if self.retour_done == True:
            return(steer,speed)

        if self.command == []:
            self.command = next(self.generator)
            self.t = time.time()
 
             
        dist_to_drive = self.command[2]
        step_done= self.checkDistDrive(dist_to_drive,self.t)
        print(step_done)
        
        if step_done == True:
            self.command = next(self.generator)
            self.t=time.time()
            self.oldx = self.x
            self.oldy = self.y

        steer = self.command[0]
        speed = self.command[1]

        #reset generator flow 
        if steer == 999:
            print("Done")
            self.retour_done = True
            self.generatorL = self.ret_flow_L()
            self.generatorR = self.ret_flow_R()
            self.generatorLR = self.ret_flow_LR()
            
        return(steer,speed)

    def checkPumperStatus(self,pumperL,pumperR,steer,speed):

        if pumperL == True and pumperR == True:
            self.retour_done = False
            self.command = []
            self.generator = self.generatorLR
        elif pumperL == True:
            self.retour_done = False
            self.command = []
            self.generator = self.generatorL
        elif pumperR == True:
            self.retour_done = False
            self.command = []
            self.generator = self.generatorR


        steer,speed=self.pumperUmfahren(steer,speed)
        return(steer,speed)
        

######################################
if __name__ == "__main__":
    
    log=Logic()

    steer,speed=log.checkPumperStatus(False,True)
    print(steer,speed)
    

    log.setRoboPos(10,100,10)
    time.sleep(0.2)

    steer,speed=log.checkPumperStatus(False,False)
    print(steer,speed)   

    log.setRoboPos(10,100,10)
    time.sleep(0.2)

    steer,speed=log.checkPumperStatus(False,False)
    print(steer,speed)



##    log.setRoboPos(0,0,10)
##    
##    log.wsa(50,100,100,1,1)
##    steer,speed=log.getCommand()
##    print(steer,speed)
##    
##    log.wsa(100,70,100,1,1)
##    steer,speed=log.getCommand()
##    print(steer,speed)
##    
##    log.wsa(100,100,100,1,1)
##    steer,speed=log.getCommand()
##    print(steer,speed)
