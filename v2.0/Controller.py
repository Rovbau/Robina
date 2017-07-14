from Client import *
from Model import *
import socket
import time
from threading import Thread
import pickle

class Controller():

    def __init__(self, model):
        self.model = model
        self.serverAddress = '127.0.0.1'
        self.running = False
        self.obstacleOffset = 0
        self.pathOffset = 0
        self.solvedPathOffset = 0

    def start(self):
        self.model.data.clearData()
        self.client = Client(self)
        try:
            self.client.connect(self.serverAddress)
            self.running = True
            self.pollingThread = Thread(target = self._poll)
            self.pollingThread.daemon = True
            self.pollingThread.start()
        except socket.error, exc:
            raise FatalException('Unable to connect to ' + self.serverAddress)

    def stop(self):
        self.running = False
        while self.polling:
            time.sleep(0.5)
        self.client.disconnect()

    def load(self, fileName):
        # load model from file
        print('loading from file ' + fileName)
        pickeln = open (fileName)
        daten= pickle.load(pickeln)
        pickeln.close()
        data = Data(daten['obstacles'],daten['path'],daten['solvedPath'])
        self.model.data.clearData()
        self.model.update(data)

    def _poll(self):
        self.polling = True
        while self.running:
            response = self.client.getData(self.obstacleOffset, self.pathOffset, self.solvedPathOffset)
            print('Received response from server: %s' % (response))
            self.obstacleOffset += len(response.obstacles)
            self.pathOffset += len(response.path)
            self.solvedPathOffset += len(response.solvedPath)
            data = Data(response.obstacles, response.path, response.solvedPath)
            self.model.update(data)
            time.sleep(10)
        self.polling = False

class FatalException(Exception):

    def __init__(self, message):
        self.message = message

    def getMessage(self):
        return(self.message)
