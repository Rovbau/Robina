import json
import socket



#ip = raw_input("IP-Adresse: ")



class Json():
    def __init__(self):
        print("Init Json")
        

    def sendVisual(self, obstacles, path, solved_path):

        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        ip = "192.168.1.103"
        #ip = "127.0.0.1"
        
        msg = json.dumps({'Obstacles': obstacles, 'Path': path, 'Solved_path': solved_path})
        try:
            send.sendto(msg, (ip, 50000)) 
            send.close()
        except:
            print("ERROR Netzwerk nicht erreichbar")
            send.close()
