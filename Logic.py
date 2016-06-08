#Logic


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
        self.pose=50
        print("Init Logic")
            
    def wsa(self,dist_front,dist_left,dist_right,pumperL,pumperR):
        """Wandering Standpoint Algorithm"""
        print("WSA")
        self.dist_front=dist_front
        self.dist_left=dist_left
        self.dist_right=dist_right
        
        if self.dist_front > 60 and self.flag_leftWall == False:
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


if __name__ == "__main__":
    
    log=Logic()

    log.setRoboPos(0,0,10)
    
    log.wsa(50,100,100,1,1)
    steer,speed=log.getCommand()
    print(steer,speed)
    
    log.wsa(100,70,100,1,1)
    steer,speed=log.getCommand()
    print(steer,speed)
    
    log.wsa(100,100,100,1,1)
    steer,speed=log.getCommand()
    print(steer,speed)
