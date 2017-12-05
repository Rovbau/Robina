import json
import sys

def createMessageFromJsonString(jsonData):
    messageName = jsonData['name'] + 'Message'

    messagesModule = sys.modules['Messages']
    messageClass = getattr(messagesModule, messageName)
    message = messageClass()
    message.deserialize(jsonData['data'])
    return message  

class Message:
    
    def serialize(self):
        messageName = self._getMessageName()
        messageData = self._getMessageData()

        message = {'name': messageName, 'data': messageData}
        return(json.dumps(message))

    def deserialize(self, data):
        pass

    def _getMessageName(self):
        return(self.__class__.__name__.replace('Message', ''))

    def _getMessageData(self):
        return({})
    
    def __str__(self):
        return(self.__class__.__name__ + '(%s)' % (self._getMessageData()))

class DisconnectMessage(Message):
    pass

class DisconnectResponseMessage(Message):
    pass

class GetDataMessage(Message):

    def __init__(self, obstacleOffset = 0, pathOffset = 0, solvedPathOffset = 0):
        self.obstacleOffset = obstacleOffset
        self.pathOffset = pathOffset
        self.solvedPathOffset = solvedPathOffset

    def _getMessageData(self):
        return({
            'obstacleOffset': self.obstacleOffset,
            'pathOffset': self.pathOffset,
            'solvedPathOffset': self.solvedPathOffset})

    def deserialize(self, data):
        self.obstacleOffset = data['obstacleOffset']
        self.pathOffset = data['pathOffset']
        self.solvedPathOffset = data['solvedPathOffset']

class DataMessage(Message):

    def __init__(self, obstacles = [[1, 1, 3], [2, 2, 1]], path = [], solvedPath = []):
        self.obstacles = obstacles
        self.path = path
        self.solvedPath = solvedPath

    def _getMessageData(self):
        return({
            'obstacles': self.obstacles,
            'path': self.path,
            'solvedPath': self.solvedPath})

    def deserialize(self, data):
        self.obstacles = data['obstacles']
        self.path = data['path']
        self.solvedPath = data['solvedPath']

    def update(self):
        self.obstacles = [[1, 1, 3], [2, 2, 1], [3, 3, 1],[4, 4, 3], [5, 5, 1], [6, 6, 1]]
        self.path = [[50, 60], [10, 80], [100, 100]]
        self.solvedPath = [[5, 0], [10, 0], [15, 0]]
        
