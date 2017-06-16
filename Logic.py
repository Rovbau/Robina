#Logic

import time
import pickle
from math import sin,cos,radians,degrees,sqrt,atan2,exp


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
        self.pose=0
        self.generatorL = self.ret_flow_L()
        self.generatorR = self.ret_flow_R()
        self.generatorLR = self.ret_flow_LR()
        self.command=[]
        self.retour_done = True
        self.stop_time = time.time()
        self.e_prev = 0
        self.ui_prev = 0
        self.timeold = time.time()
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

        if (self.dist_left < 30 or self.dist_right < 30) and ( self.flag_leftWall == False and self.flag_rightWall == False):
            self.wallMode() 
            
        return(self.steer,self.speed)

    def turnToGoal(self):
        """Wenn kein Obstacle nahe, Drehe zu Zielkurs"""
        print("GOAL")

        winkel = self.globalZielkurs()
        
        stellgroesse_ziel = self.pid_controller(winkel,self.pose)
        self.steer = stellgroesse_ziel

    def wallMode(self):
        """Wall-Modus Robo folgt Links oder Recht"""
        avoid_front = 0
        avoid_side = 0
        #Deside Wall L oder R
        if self.flag_leftWall == False and self.flag_rightWall == False:
            if self.dist_left < self.dist_right:            
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

        #calc Kurvenkomando front und side
        if self.dist_front < 70:
            avoid_front = exp(-(self.dist_front-60)*0.05)
            avoid_front = 0 - avoid_front

        avoid_side = (50.0-self.aktiv_sensorLR)/50.0
        avoid_side = avoid_side*(-1.0)
        print("Avoid-Side: "+str(avoid_side))

        self.steer = avoid_front + avoid_side

        if self.steer >= 1: self.steer = 1
        if self.steer <= -1: self.steer = -1
        
        #Beende Wall-mode       
        winkel_to_goal = self.getKursDiff(self.globalZielkurs(),self.pose)
        
        if abs(winkel_to_goal)< 25 and self.dist_front > 80 and self.dist_left > 30 and self.dist_right > 30:
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

##        soll = radians(soll)
##        ist = radians(ist)
##        winkel = atan2(sin(soll-ist),cos(soll-ist))
##        return(degrees(winkel))
    
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

    def setGlobalZiel(self, endziel_x, endziel_y):
        self.endziel_x, self.endziel_y = endziel_x, endziel_y

    def globalZielkurs(self):
        """Berechne Zielkurs anhand aktueller Pos"""
        #Diff EndzielX/Y von Pos 
        diff = (self.endziel_x - self.x, self.endziel_y - self.y)
        #Kartesisch in Polarkoordinaten
        x,y=diff
        kurs_to_globalziel=degrees(atan2(y,x))
        return(kurs_to_globalziel)
          
        
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
        actual_dist= sqrt(pow(abs(deltaX),2)+pow(abs(deltaY),2))
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

        if self.flag_leftWall == True:
            if pumperL == True or pumperR == True:
                self.retour_done = False
                self.command = []
                self.generatorL = self.ret_flow_R()
                self.generator = self.generatorR
        elif self.flag_rightWall == True:
            if pumperL == True or pumperR == True:
                self.retour_done = False
                self.command = []
                self.generatorL = self.ret_flow_L()
                self.generator = self.generatorL       
        elif self.flag_leftWall == False and self.flag_rightWall == False:
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
        
    def blocked(self, steer, speed, countsH, pumperL, pumperR):
        """Wenn Robo stillsteht starte Pumper Routine"""
        
        if pumperL == True or pumperR == True:
            return(pumperL, pumperR)
        #Wenn 3Sec keine Bewegung simuliere PumperLR=TRUE
        if (time.time()-self.stop_time) > 3:
            self.stop_time = time.time()
            print("RETOUR TIME to high")
            time.sleep(1)
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

    def pid_controller(self, soll, ist, Ki=0.001, Kd=0.001, Kp=0.025):
            """Calculate System Input using a PID Controller
            Arguments:
            ist  .. Measured Output of the System
            soll .. Desired Output of the System
            Kp .. Controller Gain Constant
            Ki .. Controller Integration Constant
            Kd .. Controller Derivation Constant
            u0 .. Initial state of the integrator
            e0 .. Initial error"""

            # Error between the desired and actual output
            e = self.getKursDiff(soll,ist)
            print(e)

            # Integration Input
            ui = self.ui_prev + Ki * e
            # Derivation Input
            ud = Kd * (e - self.e_prev)

            # Adjust previous values
            self.e_prev = e
            self.ui_prev = ui

            # Calculate output for the system
            u = Kp * (e + ui + ud)

            if u > 1: u = 1
            if u < -1: u = -1
            
            return (u)

    def save_environment(self, obst, path):
        """Sichere Path und Obstacle in File"""
        
        filename = "Stube"        
        last_save = time.time()-self.timeold
        
        if last_save > 4:           
            pickelPath=open( "EnvironmentRobo-"+filename+".p", "wb" )
            pickle.dump({'Obstacle':obst, 'Path':path}, pickelPath)
            pickelPath.close()
            self.timeold = time.time()
            
######################################
if __name__ == "__main__":
    
    log=Logic()

    log.save_environment([[2,2,4],[3,3,3]],[[10,10],[20,20]])

    log.setGlobalZiel(1000,1000)
   
    log.setRoboPos(0,0,0)
    time.sleep(0.2)

    steer,speed=log.checkPumperStatus(False,False,0,0)
    print(steer,speed)   

    log.setRoboPos(0,0,40)
    time.sleep(0.2)

    log.flag_leftWall = True
    steer, speed = log.wsa(70,40,100,False,False)
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
