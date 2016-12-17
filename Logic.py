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
        self.stop_time = time.time()        
        print("Init Logic")
            
    def wsa(self,dist_front,dist_left,dist_right,pumperL,pumperR):
        """Wandering Standpoint Algorithm"""
        self.dist_front=dist_front
        self.dist_left=dist_left
        self.dist_right=dist_right

        #Wall-Mode oder GeradeFahrt
        if self.dist_front > 70 and self.flag_leftWall == False and self.flag_rightWall == False:
            self.turnToGoal()
            self.speed=1
        else:
            self.wallMode()

        #if self.dist_left < 30 or self.dist_right < 30 or ( self.flag_leftWall == False and self.flag_rightWall == False):
        #    self.wallMode() 
            
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

        #Deside Wall L oder R
        if self.flag_leftWall == False and self.flag_rightWall == False:         
            if self.getKursDiff(self.zielkurs,self.pose) >= 0:
                self.flag_leftWall = True
                self.aktiv_sensorLR = self.dist_left
            else:
                self.flag_rightWall = True
                self.aktiv_sensorLR = self.dist_right
                
        #set activ Sensor L oder R
        if self.flag_leftWall == True:
            self.aktiv_sensorLR = self.dist_left
        else:
            self.aktiv_sensorLR = self.dist_right
            
        winkel=self.getKursDiff(self.zielkurs,self.pose)
        #print("Winkel:" +str(int(winkel)))
        
        if self.dist_front < 70:
            self.steer = -1

        if self.aktiv_sensorLR < 30:
            self.steer = -1
            
        if self.dist_front > 70 and self.aktiv_sensorLR > 40:
            self.steer = 1

        if self.aktiv_sensorLR > 30 and self.aktiv_sensorLR < 40:
            self.steer = 0
            
        if abs(winkel)< 25 and self.dist_front > 70: #and self.aktiv_sensorLR > 30:
            self.flag_leftWall = False
            self.flag_rightWall = False
            self.steer = 0
            
        #Invert Kurvenkommando wenn Right Wall
        if self.flag_rightWall == True:
            self.steer = self.steer * (-1)
            print("RIGHT WALL")
        else:
            print("LEFT WALL")
                 
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

        return(Winkel)

    def getCommand(self):
        """Return Kurs Empfehlung (steer,speed) von WSA-Algorithm"""
        return(self.steer,self.speed)

    def setRoboPos(self,x,y,pose):
        """Set Robo position (GlobX, GlobY, GlobPose) for WSA-Algorithm"""
        self.x = x
        self.y = y
        self.pose = pose

    def setZielkurs(self,kurs):
        self.zielkurs = kurs
    
        
    def ret_flow_L(self):
        """Ablauf fuer Retour wenn PumperL"""
        yield ([0,-1,5])
        yield([-1,-1,15])
        yield ([0,1,20])
        yield ([999,0,10])

    def ret_flow_R(self):
        """Ablauf fuer Retour wenn PumperR"""
        yield ([0,-1,5])
        yield([1,-1,15])
        yield ([0,1,20])
        yield ([999,0,0])

    def ret_flow_LR(self):
        """Ablauf fuer Retour wenn Pumper L+R"""
        yield ([0,-1,5])
        if  self.flag_rightWall == True:
            yield([1,-1,15])
        else:
            yield([-1,-1,15])
        yield ([0,1,20])
        yield ([999,0,10])
        
    def checkDistDrive(self,dist,t):
        """returns True if RetourDistance (dist) is Done"""

        deltaX = self.x-self.oldx
        deltaY = self.y-self.oldy
        actual_dist= math.sqrt(pow(abs(deltaX),2)+pow(abs(deltaY),2))
        #print(actual_dist)

        drive_time= time.time() - self.t
        
        if abs(actual_dist) > dist or drive_time > 5:
            dist_done=True
        else:
            dist_done=False
            
        return(dist_done)

    def pumperUmfahren(self,steer,speed):
        """Umfahre HardObstacle"""

        if self.retour_done == True:
            return(steer,speed)

        print("RETOUR MODUS")

        if self.command == []:
            self.command = next(self.generator)
            self.t = time.time()
            self.oldx = self.x
            self.oldy = self.y 
             
        dist_to_drive = self.command[2]
        step_done= self.checkDistDrive(dist_to_drive,self.t)
        
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
            steer=0
            speed=0
            
        return(steer,speed)

    def checkPumperStatus(self,pumperL,pumperR,steer,speed):
        """Starte Ausweichmanoever bei Pumper == True"""

        if pumperL == True and pumperR == True:
            self.retour_done = False
            self.command = []
            self.generatorLR = self.ret_flow_LR()
            self.generator = self.generatorLR
        elif pumperL == True:
            self.retour_done = False
            self.command = []
            self.generatorL = self.ret_flow_L()
            self.generator = self.generatorL
        elif pumperR == True:
            self.retour_done = False
            self.command = []
            self.generatorR = self.ret_flow_R()
            self.generator = self.generatorR

        steer,speed=self.pumperUmfahren(steer,speed)
        return(steer,speed)
        
    def blocked(self,steer, speed, countsH, pumperL, pumperR):
        """Wenn Robo stillsteht starte Pumper Routine"""
        
        if pumperL == True or pumperR == True:
            return(pumperL, pumperR)
        #Wenn 3Sec keine Bewegung simuliere PumperLR=TRUE
        if (time.time()-self.stop_time) > 3:
            self.stop_time = time.time()
            return(True,True)
        #Solange CountHinten zaehlt  normal weiter
        if (speed != 0 or steer  != 0) and countsH != 0:
            self.stop_time = time.time() 
            return(False, False)
        #Bei retour nicht nochmals Retour
        if  speed == -1 :
            self.stop_time = time.time()
            return(False, False)       
        return(False,False)

            
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
