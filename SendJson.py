import json
import socket



#ip = raw_input("IP-Adresse: ")
ip = "127.0.0.1"


class Json():
    def __init__(self):
        print("Init Json")
        

    def sendVisual(self, obstacles, path):

        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        ip = "192.168.1.40"

        msg = json.dumps({'Obstacles': obstacles, 'Path': path})
        send.sendto(msg, (ip, 50000)) 
        send.close()
        
