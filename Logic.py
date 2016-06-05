#Logic


class Logic():
    def __init__(self):
        """init Logic objekt"""
        self.timer=0
        print("Init Logic")

    def nextStep(self,dist_front,dist_left,dist_right,pumperL,pumperR):
        """Die amoeben Logic des Robos"""
        steer=0
        speed=0
        if pumperL == True or pumperR == True:
            self.timer=10
        
        if dist_front<60:
            steer=1
        elif dist_left<40:
            steer=-1
        elif dist_left>60 and dist_left<90:
            steer=-1       
        else:
            steer=0
            speed=1
            
        if pumperL == True or pumperR == True or self.timer>1:
            self.timer=self.timer-1
            steer=0
            speed=-1
        return(steer,speed)
            
