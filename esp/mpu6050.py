import machine
from math import atan2, degrees, sqrt

class accel():
  # __init__ initializes i2c adresses for the mpu
  def __init__(self, i2c, addr=0x68):
    self.iic = i2c
    self.addr = addr
    self.iic.start()
    self.iic.writeto(self.addr, bytearray([107, 0]))
    self.iic.stop()
  # get_raw_values reads the raw sensor data
  def get_raw_values(self):
    self.iic.start()
    a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
    self.iic.stop()
    return a

  # get_ints adds the sensor data into an array
  def get_ints(self):
    b = self.get_raw_values()
    c = []
    for i in b:
        c.append(i)
    return c

  # bytes_toint converts the bytes to values
  def bytes_toint(self, firstbyte, secondbyte):
    if not firstbyte & 0x80:
       return firstbyte << 8 | secondbyte
    return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

  # get_values converts the values to human readable acceleration values per axis and calculates the rotation from them
  def get_values(self):
    raw_ints = self.get_raw_values()
    xAc = self.bytes_toint(raw_ints[0], raw_ints[1]) / 16384.0
    yAc = self.bytes_toint(raw_ints[2], raw_ints[3]) / 16384.0
    zAc = self.bytes_toint(raw_ints[4], raw_ints[5]) / 16384.0
    xRot = self.get_x_rotation(xAc, yAc, zAc)
    yRot = self.get_y_rotation(xAc, yAc, zAc)
    return xRot, yRot
   
   # dist calculates the distance between two points in 2D space
  def dist(self, a, b):
    return sqrt((a*a)+(b*b))

  # get_y_rotation calculates the rotation around the y axis
  def get_y_rotation(self, x, y, z):
    radians = atan2(x, self.dist(y, z))
    return -degrees(radians)
	
	# get_x_rotation calculates the rotation around the x axis
  def get_x_rotation(self, x, y, z):
    radians = atan2(y, self.dist(x,z))
    return degrees(radians) 




