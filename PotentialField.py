from Tkinter import *

#Programm Zeichnet ein PotentialFeld anhand bestehenen Hindernissen auf Canvas

class PotentialField():
    def __init__(self):
        pass

    def drawField(self, obstacle_list,can):
        """Zeichne PotentialFeld anhand Obstacles"""
        Nullx=300
        Nully=300
        
        self.can = can
        self.obstacle_list = obstacle_list
        temp_list = []
        sice = 4

        #Runde Hinderniss auf 10er
        for elem in self.obstacle_list:
            x = round(elem[0],-1)
            y = round(elem[1],-1)
            temp_list.append([x,y])
        self.obstacle_list = temp_list

        #Zeichne Felder ein 
        for self.x_achse in range(-300,300,10):
            for self.y_achse in range(-300,300,10):
                force = self.countField()
                if force > 0:
                    if force > 250: force = 250
                    mycolor = '#%02x%02x%02x' % (force, 100, 200)
                    self.can.create_rectangle(Nullx+self.x_achse-sice,Nully-self.y_achse+sice,
                                              Nullx+self.x_achse+sice,Nully-self.y_achse-sice,
                                             width=0, fill=mycolor,tag="Fields")
    
    def countField(self):
        """Berechne anhand Nachbarfelder die Force (Abstosskraft)"""
        field_force = 0
        
        for delta_x in range(-30,40,10):
            for delta_y in range(-30,40,10):
                if [self.x_achse-delta_x , self.y_achse-delta_y] in self.obstacle_list:
                    field_force += 1
        return(field_force*50)


if __name__ == "__main__":

    #Tkinter 
    root=Tk()
    root.title ("Field-Daten")           #Titel de Fensters
    root.geometry("700x700+0+0")
    
    can=Canvas(master=root, width=600, height=600, bg="grey")
    can.pack()
    
    obstacle_list = [[20,25],[20,30],[105,100],[110,200],[115,100],[320,300]]
    
    potential = PotentialField()
    potential.drawField(obstacle_list,can)


    root.mainloop()
