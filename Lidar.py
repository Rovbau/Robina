import smbus
import time

class Lidar_Lite():
  def __init__(self):
    self.address = 0x62
    self.distWriteReg = 0x00
    self.distWriteVal = 0x04
    self.distReadReg1 = 0x8f
    self.distReadReg2 = 0x10
    self.velWriteReg = 0x04
    self.velWriteVal = 0x08
    self.velReadReg = 0x09
    self.status = 0x01
    print("Init Lidar")

  def connect(self, bus):
    try:
      self.bus = smbus.SMBus(bus)
      time.sleep(0.5)
      return 0
    except:
      return -1

  def writeAndWait(self, register, value):
    self.bus.write_byte_data(self.address, register, value);

  def readAndWait(self, register):
    res = self.bus.read_byte_data(self.address, register)
    return res

  def getDistance(self):
    """Read Lidar distance [cm], Waits for BusyFlag = low""" 
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    status_bit = bin(self.readAndWait(self.status))
    
    while status_bit[7] == "1":
      status_bit = bin(self.readAndWait(self.status))
      
    dist1 = self.readAndWait(self.distReadReg1)
    dist2 = self.readAndWait(self.distReadReg2)
    return (dist1 << 8) + dist2

  def getVelocity(self):
    self.writeAndWait(self.distWriteReg, self.distWriteVal)
    self.writeAndWait(self.velWriteReg, self.velWriteVal)
    vel = self.readAndWait(self.velReadReg)
    return self.signedInt(vel)

  def signedInt(self, value):
    if value > 127:
      return (256-value) * (-1)
    else:
      return value

if __name__ == "__main__":

  lidar = Lidar_Lite()
  lidar.connect(1)
  liste = []
  start = time.time()
  for  i in range(10):
    x = lidar.getDistance()
    time.sleep(0.5)    
  
    print(x)
  stop = time.time()
  print(stop-start)

  
