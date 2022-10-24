#!usr/bin/env python3

from time import sleep
from tkinter import E
from opcua import Server
from threading import Thread
from datetime import datetime
import socket
from math import tan, atan, sqrt, pi

# sth_wrong sets the everything_ok variable of the robot to "False", thus alerting the robot 
# client to stop any movement and alert the user; additionally the client variable message 
# is set to the text the robot is supposed to display on the panel
def sth_wrong(everything_ok, message, text):
    everything_ok.set_value(False)
    message.set_value(text)

def main():
    server = Server() #Server variable is initialized
    ip_address = socket.gethostbyname(socket.gethostname() + ".local") 

    server.set_endpoint(f"opc.tcp://{ip_address}:3470") # the opc ua server endpoint is set to the local ip adress of the RPi
    server.register_namespace("Horst600-Projekt") # the namespace is registered

    objects = server.get_objects_node() # assigning the objects node to a variable, so objects can be added

    sensor_master = objects.add_object('ns=2;s="sensor_master"', "Sensormaster") # adding a sensor master as an object; the mqtt_opcua_bridge client will register under this node
    temperature = sensor_master.add_variable('ns=2;s="temp"', "Aktuelle Temperatur", 25) # adding temperature as a variable to the sensor master object
    temperature.set_writable() # setting the variable to writable so the opc ua client can modify its value according to the sensor readings
    
    # adding the rotation variables to the sensor master and setting them to writable
    x_rotation = sensor_master.add_variable('ns=2;s="x_rotation"', "xRotation", 0.0) 
    x_rotation.set_writable()
    y_rotation = sensor_master.add_variable('ns=2;s="y_rotation"', "yRotation", 0.0)  
    y_rotation.set_writable()

    # adding the robot as an object; the robot client will register under this node
    horsti = objects.add_object('ns=3;s="horsti"', "HORST600") 
    # adding the everything_ok variable to the robot node; this is what the robot client will check to see
    # if it should stop movements
    everything_ok = horsti.add_variable('ns=3;s="everything_ok"', "Everything is okay", True)
    everything_ok.set_writable() #setting the variable to writable so the opc ua client can modify its value according to the sensor readings
    # adding the message variable to the robot node; this is the message that the robot client will display 
    # on the panel when something is wrong
    message = horsti.add_variable('ns=3;s="state"', "Nachricht", "Keine Nachricht!")
    message.set_writable() # setting the variable to writable so the opc ua client can modify its value according to the sensor readings

    # starting the server
    print("Starting server...")
    server.start() 
    print("Server online!")

    # reading the client variables from the sensor master and checking if they're within the acceptable 
    # range; if not, sth_wrong() is called with an appropriate message for the user    
    try:
        while True: 
            abs_rotation_rad = atan(sqrt((tan(x_rotation))**2 + (tan(y_rotation))**2))
            abs_rotation_deg = abs_rotation_rad*180/pi           
            if (temperature.get_value() > 40):
                sth_wrong(everything_ok, message, "Die Temperatur hat den zulässigen Bereich überschritten! (40°C<)")
            elif (temperature.get_value()) < 5:
                sth_wrong(everything_ok, message, "Die Temperatur hat den zulässigen Bereich unterschritten! (<5°C)")
            elif (abs_rotation_deg > 5): 
                sth_wrong(everything_ok, message, "Die Montagefläche hat die zulässige Neigung überschritten (5°)!")
            else:
                sleep(0.001)

            # if an error was detected, the server sets everything_ok to False; the program pauses until the   
            # variable is set to "True" by the robot client, which happens after the user signs the action            
            while everything_ok.get_value == False: 
                sleep(1)
                        
    except KeyboardInterrupt:
        server.stop()
        print("Server offline")


if __name__ == "__main__":
    main()