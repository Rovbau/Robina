#Karte



class Karte():
    def __init__(self):
        pass

    def updateObstacles(self,Obstacles):
        """Obstacles werden in ScanList eingetragen"""
        ScanList=[[-90,0],[-80,0],[-70,0],[-60,0],[-50,0],
                    [-40,0],[10,0],[20,0],[30,0],[40,0],[50,0]]

        for i in range(len(Obstacles)): 
            for k in range(len(ScanList)):              
                if Obstacles[i][0]==ScanList[k][0]:
                    ScanList[k][1]=Obstacles[i][1]
        return(ScanList)


if __name__ == "__main__":

    Obstacles=[[-60,110],[-50,110],[-40,130],[10,140]]

    K=Karte()
    print(K.updateObstacles(Obstacles))
    

