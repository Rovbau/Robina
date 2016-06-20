#Manuell Mode


class Manuell():
    def __init__(self):
        self.count=0

    def getTastenInput(self,steer, speed):
        """Warte auf Taste und steuere Robo gemaess Taste"""
        
        self.count += 1
        if self.count == 10:
            speed=0
            steer=0
            self.count=0
            print(self.count)

            comm=input("COMMAND PLEASE: ")
            if comm == 8:
                speed=1
                steer=0
            elif comm == 6:
                speed=0
                steer=-1
            elif comm == 4:
                speed=0
                steer=1
            elif comm == 0:
                speed=0
                steer=0
            elif comm == 2:
                speed=-1
                steer=0
            elif comm == 1:
                speed=-1
                steer=1
            elif comm == 3:
                speed=-1
                steer=-1            
            else:
                speed=0
                steer=0
        return(steer,speed)


if __name__ == "__main__":

    man = Manuell()
    while True:
        steer,speed = man.getTastenInput()
        print(steer,speed)
    

    
