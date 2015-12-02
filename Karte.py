#Karte

from math import sin,cos,radians,sqrt

class Karte():
    def __init__(self):
        self.RoboPosY=0
        self.RoboPosX=0
        self.RoboPath=[]
        GlobalKurs=0

    def updateObstacles(self,Obstacles):
        """Obstacles werden in ScanList eingetragen"""
        ScanList=[[-90,0],[-80,0],[-70,0],[-60,0],[-50,0],
                    [-40,0],[10,0],[20,0],[30,0],[40,0],[50,0]]

        for i in range(len(Obstacles)): 
            for k in range(len(ScanList)):              
                if Obstacles[i][0]==ScanList[k][0]:
                    ScanList[k][1]=Obstacles[i][1]
        return(ScanList)



    def updateRoboPos(self,DeltaDist,SteerDiff,KompassCourse):
        """Update Robo Position auf Karte"""

        #RoboSchwerpunkt bis Rad mm
        a=180   
        c=180
        
        self.KursBeiStart=KompassCourse
        WinkelDiff=SteerDiff*5.2    #Counts in Winkle umwandeln
        

        if SteerDiff != 0:
            #Kosinussatz: Schwerpunkt Wegversatz berechnen
            b=sqrt(pow(a,2)+pow(c,2)-2*a*c*cos(radians(WinkelDiff)))

            #Richtung des Wegversatz in GlobalKurs umrechnen
            GlobalKurs=self.KursBeiStart+WinkelDiff
            if GlobalKurs>360:
                GlobalKurs=GlobalKurs-360
            if GlobalKurs<0:
                GlobalKurs=360-abs(GlobalKurs)
                

            #Position des Robo auf Karte updaten
            self.RoboPosY=b*sin(radians(GlobalKurs))+self.RoboPosY
            self.RoboPosX=b*cos(radians(GlobalKurs))+self.RoboPosX


        if SteerDiff == 0 and DeltaDist != 0:
            #Position des Robo auf Karte updaten
            self.RoboPosX=DeltaDist*sin(radians(self.KursBeiStart))+self.RoboPosX
            self.RoboPosY=DeltaDist*cos(radians(self.KursBeiStart))+self.RoboPosY
       
        self.RoboPath.append([round(self.RoboPosX,1),round(self.RoboPosY,1)])


    def getRoboPos(self):
        """returns RoboPos X,Y"""
        return(round(self.RoboPosX,1),round(self.RoboPosY,1))
    
    def getRoboPath(self):
        """returns RoboPos X,Y"""
        return(self.RoboPath)

if __name__ == "__main__":

    Obstacles=[[-60,110],[-50,110],[-40,130],[10,140]]
    K=Karte()
    print(K.updateObstacles(Obstacles))
    
    DeltaDist=10
    SteerDiff=0
    KompassCourse=0
    K.updateRoboPos(DeltaDist,SteerDiff,KompassCourse)

    DeltaDist=5
    SteerDiff=0
    KompassCourse=90
    K.updateRoboPos(DeltaDist,SteerDiff,KompassCourse)
    
    print(K.getRoboPos())
    print(K.getRoboPath())








    
    

