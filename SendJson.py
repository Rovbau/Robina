import json
import socket



#ip = raw_input("IP-Adresse: ")



class Json():
    def __init__(self):
        print("Init Json")
        

    def sendVisual(self, obstacles, path, solved_path):

        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        ip = "192.168.4.165"

        msg = json.dumps({'Obstacles': obstacles, 'Path': path, 'Solved_path': solved_path})
        send.sendto(msg, (ip, 50000)) 
        send.close()
        
