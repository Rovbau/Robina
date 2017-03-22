#Erzeugt Grid Basics

#([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

from copy import deepcopy
import cPickle as pickle
from Astar import *

class Grid():
    def __init__(self, width, heigh):
        self.width=width
        self.heigh=heigh
        self.walls=[[1,2,3,],[2,3,4]]
        self.gridwithweights=GridWithWeights(width,heigh)
        self.clearance_add_walls=[]
        self.last_start_pos=(width,heigh)
        
        
    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles
        self.roundet_walls=[]
        
        for obstacle in unpaintedObstacles:
            element_allready = False
            #round to 5 Bsp: x=int(round(obstacle[0]/5.0)*5.0)
            obstacle_x_grid = int(obstacle[0]/10)
            obstacle_y_grid = int(obstacle[1]/10)
            print("Ein Obstacle")
            for element in self.walls:
                if element[0:2] == [obstacle_x_grid,obstacle_y_grid]:
                    element[2] = element[2]+1
                    self.roundet_walls.append(element)
                    print("Element Plus 1")
                    element_allready = True
                    break
            if element_allready == False:
                    self.walls.append([obstacle_x_grid,obstacle_y_grid,1])
                    self.gridwithweights.walls=deepcopy(self.walls)
                    self.roundet_walls.append([obstacle_x_grid,obstacle_y_grid,1])
                    print("Schon vorhanden")
                                        
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
        x=int(x/10)
        y=int(y/10)
        self.startgrid=(x,y)
        
    def setZielInGrid(self,x,y):
        x=int(x/10)
        y=int(y/10)
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
        #print(self.gridwithweights.walls)
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
            print("SUCHE Path zo Ziel: ")
            motor.setCommand(steer,speed)
            return(self.path)
        except:
            print("ERROR")
            print("Grid-Aktual:" +str(self.startgrid))
            print("Grid-Ziel:" +str(self.zielgrid))
            #print(self.came_from)
            #print(self.gridwithweights.walls)
            motor.setCommand(steer,speed)

    def saveGridPath(self,path):
        """Path speichern pickle"""
        pickleSolved=open( "RoboSolved.p", "wb" )
        pickle.dump(path,pickleSolved)
        pickleSolved.close()
    
    def drawSolvedPath(self):
        print(self.startgrid)
        draw_grid(self.gridwithweights, width=1, point_to=self.came_from, start=self.startgrid,
                  goal=self.zielgrid)


if __name__ == "__main__":

    g = Grid(100,100)
    g.setStartInGrid(20,20)
    g.setZielInGrid(80,80)

    g.obstaclesInGrid([[70, 80],[90, 80],[80, 70],[80, 90]])    
    #g.addClearance()
    print(g.walls)
    print("***")
    weg=g.getSolvedPath(1,1,1)
    print(weg)
    g.drawSolvedPath()
    g.saveGridPath(weg)

