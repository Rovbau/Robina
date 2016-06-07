#Logic


class Logic():
    def __init__(self):
        """init Logic objekt"""
        self.timer=0
        self.steer=0
        self.speed=0
        self.flag_leftWall=False
        self.zielkurs=0
        self.x=0
        self.y=0
        self.pose=50
        print("Init Logic")

    def nextStep(self,dist_front,dist_left,dist_right,pumperL,pumperR):
        """Die amoeben Logic des Robos"""
        steer=0
        speed=0
        if pumperL == True or pumperR == True:
            self.timer=10
        
        if dist_front<60:
            steer=1
        elif dist_left<40:
            steer=-1
        elif dist_left>60 and dist_left<90:
            steer=-1       
        else:
            steer=0
            speed=1
            
        if pumperL == True or pumperR == True or self.timer>1:
            self.timer=self.timer-1
            steer=0
            speed=-1
        return(steer,speed)


            
    def wsa(self,dist_front,dist_left,dist_right,pumperL,pumperR):
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

        print("GOAL")
        winkel=self.getKursDiff(self.zielkurs,self.pose)
        
        if winkel > 10:
            self.steer=1
        elif winkel < -10:
            self.steer=-1
        else:
            self.steer=0
        
    def wallMode(self):
        print("WALL")
        self.flag_leftWall = True
        winkel=self.getKursDiff(self.zielkurs,self.pose)
        
        if self.dist_front < 70:
            self.steer = -1
            
        if self.dist_left < 30:
            self.steer = -1
            
        if self.dist_front > 70 and self.dist_left > 40:
            self.steer = 1

        if self.dist_left > 30 and self.dist_left < 40:
            self.steer = 0
            
        if abs(winkel)< 10 and self.dist_front > 70 and self.dist_left > 70:
            self.flag_leftWall = False
            self.steer = 0
            
        print(self.flag_leftWall)
        
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
        return(self.steer,self.speed)

    def setRoboPos(self,x,y,pose):
        self.x = x
        self.y = y
        self.pose = pose


if __name__ == "__main__":

    log=Logic()
    log.wsa(50,100,100)
    steer,speed=log.getCommand()
    print(steer,speed)
    
    log.wsa(100,70,100)
    steer,speed=log.getCommand()
    print(steer,speed)
    
    log.wsa(100,100,100)
    steer,speed=log.getCommand()
    print(steer,speed)
