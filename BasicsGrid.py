#Erzeugt Grid Basics

#([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

from copy import deepcopy
import pickle
from Grid import *

class Grid():
    def __init__(self, width, heigh):
        self.width=width
        self.heigh=heigh
        self.walls=[]
        self.gridwithweights=GridWithWeights(width,heigh)
        
        
    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles

        for obstacle in unpaintedObstacles:
            obstacle_x_grid=int(obstacle[0]/10)
            obstacle_y_grid=int(obstacle[1]/10)
            
            if (obstacle_x_grid,obstacle_y_grid) not in  self.walls:
                self.walls.append((obstacle_x_grid,obstacle_y_grid))

        #Hindernisse speichern            
        pickelObstacles=open( "RoboObstacles.p", "wb" )
        pickle.dump(self.walls,pickelObstacles)


    def setRoboInGrid(self,x,y):
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
                self.walls.append((x+1,y))
            if (x-1,y) not in temp_walls:
                self.walls.append((x-1,y))
            if (x,y+1) not in temp_walls:
                self.walls.append((x,y+1))
            if (x,y-1) not in temp_walls:
                self.walls.append((x,y-1))
                
            self.gridwithweights.walls=self.walls

    def getSolvedPath(self):
        """Calculate path in grid"""        
        came_from, cost_so_far = a_star_search(self.gridwithweights,
                                                   self.startgrid, self.zielgrid)
        path=reconstruct_path(came_from, self.startgrid, self.zielgrid)
        draw_grid(g.gridwithweights, width=2, point_to=came_from, start=(2,2),goal=(7,2))
        return(path)


if __name__ == "__main__":

    g = Grid(10, 10)
    g.setRoboInGrid(2,2)
    g.setZielInGrid(7,2)
    g.obstaclesInGrid([(40, 20)])    
    g.addClearance()
    print(g.walls)

    print(g.getSolvedPath())
   

