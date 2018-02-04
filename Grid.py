#! python
#Erzeugt Grid Basics

#([(0, 50),(10, 50),(20, 50),(30, 50),(40, 50),(90, 90)])

from copy import deepcopy
import cPickle as pickle
#from Astar import *
import math
import numpy as np
import sys

class Grid():
    def __init__(self, width, heigh):
        self.width = width
        self.heigh = heigh
        self.walls = []
        #self.gridwithweights=GridWithWeights(width,heigh)
        self.clearance_add_walls = []
        self.last_start_pos = (width,heigh)
        self.karten_arr = np.zeros(shape = (self.width, self.heigh))
        self.x_middle = self.width / 2
        self.y_middle = self.heigh / 2         
        
    def obstaclesInGrid(self, obstacles):
        """GlobaleHinderniss (x[cm],y[cm]) in Grid eintragen (RasterX,RasterY)"""        
        unpaintedObstacles=obstacles
        self.roundet_walls=[]
        neg_element = []
        
        for obstacle in unpaintedObstacles:
            
            #round to 5 Bsp: x=int(round(obstacle[0]/5.0)*5.0)
            obstacle_x_grid = int(obstacle[0]/10)
            obstacle_y_grid = int(obstacle[1]/10)
            obstacle_x_grid = obstacle_x_grid + self.x_middle
            obstacle_y_grid = obstacle_y_grid + self.y_middle
            x_occ_pre = obstacle_x_grid
            y_occ_pre = obstacle_y_grid

#************************
            x_start, y_start = self.startgrid
            x_start = x_start + self.x_middle
            y_start = y_start + self.y_middle
            hinderniss = self.karten_arr[obstacle_x_grid, obstacle_y_grid] + 10 #Add Value zu Hinderniss
            self.karten_arr[obstacle_x_grid, obstacle_y_grid] = hinderniss
            
            self.check_for_double(obstacle_x_grid, obstacle_y_grid)                         #Keine doppel
            
            print("start" +str(x_start))
            dist, winkel = self.cart2pol(obstacle_x_grid -  x_start, obstacle_y_grid - y_start)
            print(dist, winkel)

            for distance in range(0, int(round(dist))):                                 #Von dist=0 bis zum Hinderniss
                x_occ, y_occ = self.pol2cart(distance, winkel)
                print(x_occ, y_occ)
                
                if x_occ != x_occ_pre or  y_occ != y_occ_pre:
                    self.karten_arr[x_occ + x_start ,y_occ + y_start] = self.karten_arr[x_occ + x_start ,y_occ + y_start] - 1     #Reduziere Feldwert da kein Hinderniss
                    x_occ_pre, y_occ_pre = x_occ, y_occ

                    self.check_for_double(x_occ + x_start ,y_occ + y_start)                                 #Keine doppel in roundet_walls
            
        print(self.karten_arr)
        print(sys.getsizeof(self.karten_arr))
        print(sys.getsizeof(self.roundet_walls))
        
    def check_for_double(self,x_occ, y_occ):
        x_occ = x_occ - self.x_middle
        y_occ = y_occ - self.y_middle
        element_allready = False
        for element in self.roundet_walls:                                  #Keine doppel in roundet_walls
            element_allready = False
            if element[0:2] == [x_occ, y_occ]:
                element[2] = self.karten_arr[x_occ, y_occ]
                element_allready = True
                break                           
        if element_allready == False:                                       #Add neue Felder zu roundet_walls
            self.walls.append([x_occ, y_occ,1])
            #self.gridwithweights.walls=deepcopy(self.walls)
            self.roundet_walls.append([x_occ, y_occ, self.karten_arr[x_occ + self.x_middle, y_occ + self.x_middle]])

    def cart2pol(self, x, y):
        dist = math.sqrt(x**2 + y**2)
        winkel = math.atan2(y, x)
        return(dist, winkel)

    def pol2cart(self, dist, winkel):
        x = dist * math.cos(winkel)
        y = dist * math.sin(winkel)
        return(int(round(x)), int(round(y)))
                                   
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

    def getGridObstacles(self):
        return(self.gridwithweights.walls)

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

        #motor.setCommand(0,0)
        #print(self.gridwithweights.walls)
        #No Wall on Robo-Ist position
        #if self.startgrid in self.gridwithweights.walls:
        #    self.gridwithweights.walls.remove(self.startgrid)
         #   print("Del StartPosi in Grid")
            
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

    g = Grid(12,12)
    g.setStartInGrid(30,30)
    g.setZielInGrid(80,80)

    g.obstaclesInGrid([[-50, -50]])    #,[80, 80],[80, 70],[80, 90]

    #g.addClearance()
    print(sorted(g.getRoundetWalls()))
    print("***")
    #weg=g.getSolvedPath(1,1,1)
    #print(weg)
    #g.drawSolvedPath()
    #g.saveGridPath(weg)

