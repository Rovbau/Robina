#Erzeugt Grid Basics

#([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

from copy import deepcopy
import pickle
from Astar import *

class Grid():
    def __init__(self, width, heigh):
        self.width=width
        self.heigh=heigh
        self.walls=[]
        self.gridwithweights=GridWithWeights(width,heigh)
        self.clearance_add_walls=[]
        self.last_start_pos=(width,heigh)
        
        
    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles
        
        for obstacle in unpaintedObstacles:
            obstacle_x_grid=int(obstacle[0]/10)
            obstacle_y_grid=int(obstacle[1]/10)
            
            if (obstacle_x_grid,obstacle_y_grid) not in  self.walls:
                self.walls.append((obstacle_x_grid,obstacle_y_grid))
                self.gridwithweights.walls=deepcopy(self.walls)


    def saveGridObstacles(self):
        """Hindernisse speichern pickle"""
        pickelObstacles=open( "RoboObstacles.p", "wb" )
        pickle.dump(self.walls,pickelObstacles)
        pickelObstacles.close()

    def setStartInGrid(self,x,y):
        self.startgrid=(x,y)
        
    def setZielInGrid(self,x,y):
        self.zielgrid=(x,y)
        
    def addClearance(self):
        """Adds clearance for every Wall"""
        temp_walls=deepcopy(self.walls)

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
                
            self.gridwithweights.walls=deepcopy(temp_walls)

    def getSolvedPath(self):
        """Calculate path in grid"""
        #Calc only when Grid-Pos changed
        if self.startgrid == self.last_start_pos:
            return(self.path)
        self.last_start_pos=self.startgrid

        print("SUCHE...Weg")
        
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
            return(self.path)
        except:
            print("ERROR")
            print(self.startgrid)
            print(self.zielgrid)
            print(self.came_from)
            print(self.gridwithweights.walls)
        

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

