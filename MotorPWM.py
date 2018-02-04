# Simple two DC motor PWM robot class

import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT


class MotorPWM(object):
    def __init__(self, addr=0x60, left_id=1, right_id=2, left_trim=0, right_trim=0,
                 stop_at_exit=True):
        self.e_prev = 0
        self.ui_prev = 0
        self.motor_backward = None
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - left_id: The ID of the left motor, default is 1.
         - right_id: The ID of the right motor, default is 2.
         - left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Adafruit_MotorHAT(addr)
        self._left = self._mh.getMotor(left_id)
        self._right = self._mh.getMotor(right_id)
        self._left_trim = left_trim
        self._right_trim = right_trim
        # Start with motors turned off.
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def setCommand(self,steer,speed, actual_speed_L = None, actual_speed_R = None):
        """MotorPWM Command. -1< steer >1 und -1< speed >1"""
        speedL = 0
        speedR = 0
        
        #Kurve berechnen
        if steer >= 0:
            speedL = 127 - steer*127
            speedR = 127
        else:
            speedL = 127
            speedR = 127 + steer*127
            
        #Soll Speed 
        speedL = speedL*abs(speed)
        speedR = speedR*abs(speed)

        #PID auschalten wenn acutual None
        if actual_speed_L and actual_speed_R != None:
            #Negativen ist-speed verhindern
            actual_speed_L = abs(actual_speed_L)
            actual_speed_R = abs(actual_speed_R)

        #Vor oder Zurueck
        if  speed > 0:
            speedL = self.pid_pwm_controller(speedL, actual_speed_L)
            speedR = self.pid_pwm_controller(speedR, actual_speed_R)
           
            self._left_speed(int(speedL))
            self._right_speed(int(speedR))
            self._left.run(Adafruit_MotorHAT.FORWARD)
            self._right.run(Adafruit_MotorHAT.FORWARD)
            self.motor_backward = False
        elif speed < 0:
            speedL = self.pid_pwm_controller(speedL, actual_speed_L)
            speedR = self.pid_pwm_controller(speedR, actual_speed_R)
            
            self._left_speed(int(speedL))
            self._right_speed(int(speedR))
            self._left.run(Adafruit_MotorHAT.BACKWARD)
            self._right.run(Adafruit_MotorHAT.BACKWARD)
            self.motor_backward = True
        elif speed == 0:
            self._left.run(Adafruit_MotorHAT.RELEASE)
            self._right.run(Adafruit_MotorHAT.RELEASE)
            self.motor_backward = False
            
        print("PWM-PID: "+str(int(speedL))+" "+str(int(speedR))) 


    def pid_pwm_controller(self, soll, ist, Ki=0.2, Kd=0.01, Kp=0.3):
            """Calculate System Input using a PID Controller
            Arguments:
            ist  .. Measured Output of the System
            soll .. Desired Output of the System
            Kp .. Controller Gain Constant
            Ki .. Controller Integration Constant
            Kd .. Controller Derivation Constant
            u0 .. Initial state of the integrator
            e0 .. Initial error"""

            #No PID wenn kein Sollwert
            if ist == None:
                return(soll)
                
            # Error between the desired and actual output
            ist = ist * 1
            e = soll - ist

            # Integration Input
            ui = self.ui_prev + Ki * e

            # Derivation Input
            ud = Kd * (e - self.e_prev)

            # Adjust previous values
            self.e_prev = e
            self.ui_prev = ui

            # Calculate output for the system
            u = Kp * (e + ui + ud)
            u = u + soll

            if u >= 255:
                u = 255
                self.ui_prev = self.ui_prev - Ki * e  # I-Anteil begrenzen
            if u <= 0:
                u = 0
                self.ui_prev = self.ui_prev - Ki * e  # I-Anteil begrenzen
            return (u) 

    def motor_is_backward(self):
        """Returns TRUE wenn Motor retour"""
        return(self.motor_backward)

    
    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._left_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._left.setSpeed(speed)

    def _right_speed(self, speed):
        """Set the speed of the right motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._right_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._right.setSpeed(speed)

    def stop(self):
        """Stop all movement."""
        self._left.run(Adafruit_MotorHAT.RELEASE)
        self._right.run(Adafruit_MotorHAT.RELEASE)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.FORWARD)
        self._right.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._left_speed(speed)
        self._right_speed(speed)
        self._left.run(Adafruit_MotorHAT.BACKWARD)
        self._right.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

            

            
### MAIN ###
    
if __name__ == "__main__":

    motor_pwm = MotorPWM()

    motor_pwm.setCommand(0.5,1)
    time.sleep(2)
    motor_pwm.setCommand(0.0,0)    
    time.sleep(2)
    motor_pwm.setCommand(-0.5,-0.5)
    time.sleep(2)



    
