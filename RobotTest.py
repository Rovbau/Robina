# Simple two DC motor robot class usage example.
# Starten nur in Shell mit "sudo"
import time
import Robot
from threading import *
from Encoder import *
encoder = Encoder()
ThreadEncoder=Thread(target=encoder.runAllTime,args=())
ThreadEncoder.daemon=True
ThreadEncoder.start()


# Create an instance of the robot. Adress 0x60. Motor 1 and 2 default
robot = Robot.Robot(left_trim=0, right_trim=0)

##robot.forward(150, 2)   # Move forward at speed 150 for 1 second.
##robot.left(200, 2)      # Spin left at speed 200 for 0.5 seconds.
##robot.right(50, 2)  
##robot.backward(150, 2)

sleep(1)
error = 1
di = 1
#robot.curve(150,100)
while True:
   
    l,r =encoder.getPulseLR()
    encoder.clearEncoderLR()
    print("pulseL: "+str(l))
    soll = 9
    k = 5
    error = soll - l
    print("error: "+str(error))
    #error = (soll - l)*k
    if l > soll:
        di = di - 15
        print("jkjjh")
    if l < soll:
        di =  di + 15
        
    stellg = error + di 
    if stellg > 255:
        stellg = 255
    if stellg < 0:
        stellg = 0
    print("Stellg: "+str(stellg))
    robot.curve(stellg,0)
    sleep(0.5)

# Spin in place slowly for a few seconds.
#robot.forward(30)  # No time is specified so the robot will start spinning forever.
time.sleep(8.0)   # Pause for a few seconds while the robot spins (you could do
                  # other processing here though!).
robot.stop()      # Stop the robot from moving.

