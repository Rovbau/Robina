import socket
import json
from Messages import *

class Client():

    def __init__(self, controller):
        self.controller = controller
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def connect(self, address, port = 50000):
        self.socket.connect((address, port))

    def disconnect(self):
        message = DisconnectMessage()
        self._sendMessage(message)
        self.socket.close()

    def getData(self, obstacleOffset, pathOffset, solvedPathOffset):
        print('Retrieving data for obstacleOffset=%d, pathOffset=%d, solvedPathOffset=%d' % (obstacleOffset, pathOffset, solvedPathOffset))
        message = GetDataMessage(obstacleOffset, pathOffset, solvedPathOffset)
        return(self._sendMessage(message))

    def _sendMessage(self, message):
        self.socket.sendall(message.serialize())
        data = self.socket.recv(1024)
        jsonData = json.loads(data)
        message = createMessageFromJsonString(jsonData)
        return(message)

        
