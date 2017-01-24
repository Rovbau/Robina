#Erzeugt Grid Basics

#([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

from copy import deepcopy
import cPickle as pickle
from Astar import *

class Grid():
    def __init__(self, width, heigh):
        self.gridsize= 5
        self.width=width/self.gridsize
        self.heigh=heigh/self.gridsize
        self.walls=[]
        self.gridwithweights=GridWithWeights(width,heigh)
        self.clearance_add_walls=[]
        self.last_start_pos=(width,heigh)
        
        
    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles
        self.roundet_walls=[]
        
        for obstacle in unpaintedObstacles:
            #round to _5
            obstacle_x_grid=int(round(obstacle[0]/5.0)*5.0)
            obstacle_y_grid=int(round(obstacle[1]/5.0)*5.0)
            
            if (obstacle_x_grid,obstacle_y_grid) not in  self.walls:
                self.walls.append((obstacle_x_grid,obstacle_y_grid))
                self.gridwithweights.walls=deepcopy(self.walls)
                self.roundet_walls.append((obstacle_x_grid,obstacle_y_grid))

    def getRoundetWalls(self):
        return(self.roundet_walls)

    def obstacleNear(self):
        """Wenn obstacle in range, drive back"""
        x,y=self.startgrid
        range_near=3
        drive_back=False
        
        for nearx in range(x-range_near,x+range_near):
            for neary in range(y-range_near,y+range_near):
                if (nearx,neary) in self.gridwithweights.walls:
                    drive_back=True
                else:
                    drive_back=False                    
        return(drive_back)


    def saveGridObstacles(self):
        """Hindernisse speichern pickle"""
        pickelObstacles=open( "RoboObstacles.p", "wb" )
        pickle.dump(self.gridwithweights.walls,pickelObstacles)
        pickelObstacles.close()

    def setStartInGrid(self,x,y):
        """Aktuelle GridPosition uebernehmen cm -> 5cmGrid"""
        x=int(x/self.gridsize)
        y=int(y/self.gridsize)
        self.startgrid=(x,y)
        
    def setZielInGrid(self,x,y):
        x=int(x/self.gridsize)
        y=int(y/self.gridsize)
        self.zielgrid=(x,y)
        
    def addClearance(self):
        """Adds clearance for every Wall"""
        temp_walls=self.walls

        for wall in temp_walls:
            x=wall[0]
            y=wall[1]
            if (x+1,y) not in temp_walls:
                self.clearance_add_walls.append((x+1,y))
            if (x-1,y) not in temp_walls:
                self.clearance_add_walls.append((x-1,y))
            if (x,y+1) not in temp_walls:
                self.clearance_add_walls.append((x,y+1))
            if (x,y-1) not in temp_walls:
                self.clearance_add_walls.append((x,y-1))
                
        self.gridwithweights.walls=temp_walls+self.clearance_add_walls
        self.clearance_add_walls=[]

    def getSolvedPath(self,steer,speed,motor):
        """Calculate path in grid"""
        #Calc only when Grid-Pos changed
        if self.startgrid == self.last_start_pos:
            return(self.path)
        self.last_start_pos=self.startgrid

        print("SUCHE...Weg")

        motor.setCommand(0,0)
        
        #No Wall on Robo-Ist position
        if self.startgrid in self.gridwithweights.walls:
            self.gridwithweights.walls.remove(self.startgrid)
            print("Del StartPosi in Grid")
            
        #No Wall on Robo-Ziel position
        if self.zielgrid in self.gridwithweights.walls:
            print("no SPACE IN grid")
            
        self.came_from, self.cost_so_far = a_star_search(self.gridwithweights,
                                                   self.startgrid, self.zielgrid)

        try:
            self.path=reconstruct_path(self.came_from, self.startgrid, self.zielgrid)
            motor.setCommand(steer,speed)
            return(self.path)
        except:
            print("ERROR")
            print(self.startgrid)
            print(self.zielgrid)
            print(self.came_from)
            print(self.gridwithweights.walls)
            motor.setCommand(steer,speed)

    def saveGridPath(self,path):
        """Path speichern pickle"""
        pickleSolved=open( "RoboSolved.p", "wb" )
        pickle.dump(path,pickleSolved)
        pickleSolved.close()
    
    def drawSolvedPath(self):
        print(self.startgrid)
        draw_grid(self.gridwithweights, width=2, point_to=self.came_from, start=self.startgrid,
                  goal=self.zielgrid)


if __name__ == "__main__":

    g = Grid(10,10)
    g.setStartInGrid(2,2)
    g.setZielInGrid(8,8)

    g.obstaclesInGrid([[70, 80],[90, 80],[80, 70],[80, 90]])    
    #g.addClearance()
    print(g.walls)
    print("***")
    weg=g.getSolvedPath()
    print(weg)
    g.drawSolvedPath()
    g.saveGridPath(weg)

