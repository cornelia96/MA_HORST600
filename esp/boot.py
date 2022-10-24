# boot file runs on the esp everytime it boots

import network, socket, esp, gc, os, mpu6050
from machine import Pin, ADC, SoftI2C 
from math import log
esp.osdebug(None)
from time import sleep
from umqtt.simple import MQTTClient

gc.collect()

# information for esp to log into wifi
ssid = 'enter wifi ssid (name) here'
password = 'enter wifi password here'

# connecting to wifi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass

print(station.ifconfig())

# setting the necessary constants 
thermistor_pin = 34 # change to the pin you are using
dlight_barrier_pin = 35 # change to the pin you are using
BETA = 4095 # value necessary for temperature conversion
KELVIN_CONSTANT = 273.15 # value necessary for temperature conversion
ADC_VALUE = 3950 # value necessary for temperature conversion
SERVER = 'enter ip address of mqtt broker here'
# names of MQTT topics under which sensor data will be published in main.py
CLIENT_ID ='ESP32_TempSens'
TOPIC_TEMP = 'temperature'
TOPIC_XROT = 'x-rotation'
TOPIC_YROT = 'y-rotation'
TOPIC_IR = 'ir_sensor'
TOPIC_MSG = 'message'