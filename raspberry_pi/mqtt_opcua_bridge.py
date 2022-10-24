#!usr/bin/env python3

from paho.mqtt import client as mqtt
from time import sleep
from opcua import Client
import socket

IP_ADRESS = socket.gethostbyname(socket.gethostname() + ".local") # using the local ip adress of the RPi, since the opc ua client and server are on the same device

# opcuaClientConnect initializes an opc ua client and connects it to the server
def opcuaClientConnect():
    opcua_client = Client(f"{IP_ADRESS}:3470") 
    opcua_client.connect()
    opcua_client.get_namespace_array()
    objects = opcua_client.get_objects_node()
    # initializing client objects and their variables
    esp = objects.get_children()[1]
    temperature = esp.get_children()[0]
    xRot = esp.get_children()[1]
    yRot = esp.get_children()[2]
    return temperature, xRot, yRot

# on_message is called when a message is published by another mqtt client under a subscribed topic
def on_message(client, userdata, message):
    topic = message.topic
    # checking which topic the message was sent under and setting the appropriate opc ua client variable with the message value
    if topic == "temperature":
        temperature.set_value(int(message.payload))
    elif topic == "x-rotation":
        xRot.set_value(int(message))
    elif topic == "y-rotation":
        xRot.set_value(int(message))

while True:
    try:
        temperature, xRot, yRot = opcuaClientConnect()
        break
    except:
        print("OPC Server not yet available! Still waiting...") # may happen when opc ua server hasn't initialized successfully yet
        sleep(5)    


mqqt_client = mqtt.Client("translator") # initializing mqtt client

mqqt_client.connect("localhost") # using localhost as the broker is set up on the same device (Raspberry Pi)

# subscribing to the sensor topics
mqqt_client.subscribe("temperature")
mqqt_client.subscribe("x-rotation")
mqqt_client.subscribe("y-rotation")

# starting a loop to listen for messages from the broker
mqqt_client.loop_start
mqqt_client.on_message = on_message
mqqt_client.loop_forever()
