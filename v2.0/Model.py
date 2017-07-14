class Model():

    def __init__(self):
        self.data = Data()
        self.observer = []

    def update(self, data):
        print(len(self.data.obstacles))
        self.data.obstacles.extend(data.obstacles)
        self.data.path.extend(data.path)
        self.data.solvedPath.extend(data.solvedPath)
        self._notifyObservers()

    def addObserver(self, observer):
        self.observer.append(observer)

    def removeObserver(self, observer):
        self.observer.remove(observer)

    def _notifyObservers(self):
        for observer in self.observer:
            print('observer sendet'+str(observer))
            observer.notify()

class Data():

    def __init__(self, obstacles = [], path = [], solvedPath = []):
        self.obstacles = obstacles
        self.path = path
        self.solvedPath = solvedPath

    def clearData(self):
        self.obstacles = []
        self.path = []
        self.solvedPath = []
        
