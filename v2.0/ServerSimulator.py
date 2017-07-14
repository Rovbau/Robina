import SocketServer
import json
from Messages import *

class ServerSimulatorHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        response = DataMessage()
        x = 0
        connectionOpen = True
        while connectionOpen:
            data = self.request.recv(1024).strip()
            jsonData = json.loads(data)
            print('Retrieving message of type %s with data %s from client' % (jsonData['name'], jsonData['data']))
            message = createMessageFromJsonString(jsonData)

            x += 1
            if x == 3:
                response.update()
                print("Asynchrone Response updaten !")

            if 'GetDataMessage' == message.__class__.__name__:
                response.obstacles = response.obstacles[message.obstacleOffset: ]
                response.path = response.path[message.pathOffset: ]
                response.solvedPath = response.solvedPath[message.solvedPathOffset: ]
                self.request.sendall(response.serialize())
            elif 'DisconnectMessage' == message.__class__.__name__:
                print('Client disconnected')
                response = DisconnectResponseMessage()
                self.request.sendall(response.serialize())
                connectionOpen = False
                
        
        # self.request is the TCP socket connected to the client
        #self.data = self.request.recv(1024).strip()
        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

      

if __name__ == '__main__':
    print('Starting ServerSimulator')                
    server = SocketServer.TCPServer(('127.0.0.1', 50000), ServerSimulatorHandler)
    server.serve_forever()
