#!usr/bin/env python3

import xmlrpc.client
from paho.mqtt import client as mqtt
from time import time_ns, sleep
from sys import exit, argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QWidget

class Horst:
    def __init__(self, user="horstFX", password="WZA3P9", url="192.168.111.62:8080/xml-rpc"):
        self.URL = "@" + url
        '''Username and password (only needed for some calls, including RobotMoveCalls)'''
        self.USERNAME = user
        self.PASSWORD = password
        '''Construct a client with the HorstFX server url, username and password '''
        self.client = xmlrpc.client.ServerProxy("http://" + self.USERNAME + ":" + self.PASSWORD + self.URL)
        print("Initialized xmlrpc client for user '" + self.USERNAME + "'")

    def pause(self):
        self.client.HorstFX.Program.pause()

    def isRunning(self):
        self.client.HorstFX.Program.isRunning()

    def abort(self):
        self.client.HorstFX.Program.abort()

    def proceed(self):
        self.client.HorstFX.Program.proceed()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.everything_ok = True

        self.setWindowTitle("Fehlermeldung")

        self.message_label = QLabel()
        
        self.continue_btn = QPushButton("Fortsetzen")
        self.continue_btn.setCheckable(True)
        self.continue_btn.released.connect(self.continue_horst_program)

        self.cancel_btn = QPushButton("Abbrechen")
        self.cancel_btn.setCheckable(True)
        self.cancel_btn.released.connect(self.cancel_horst_program)

        self.layout = QGridLayout()
        self.layout.addWidget(self.message_label, 0, 0)
        self.layout.addWidget(self.continue_btn, 1, 0)
        self.layout.addWidget(self.cancel_btn, 1, 1)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def connect_horst(self):
        while True: 
            try:
                self.horsti = Horst()
                break
            except: 
                print("I tried to connect to HORST600!")
                sleep(1)

    def continue_horst_program(self):
        self.close()
        self.everything_ok = True 
        
    def cancel_horst_program(self):
        self.close()
        self.everything_ok = False

def on_message(client, userdata, message):
    topic = message.topic
    try:
        message = float(message.payload.decode("utf-8"))
        if (topic == "temperature" and message>40) :
            pause_horsti("Die Temperatur hat den zulässigen Bereich überschritten! (40°C<)")
        elif (topic == "temperature" and message<5) :
            pause_horsti("Die Temperatur hat den zulässigen Bereich unterschritten! (<5°C)")
        elif (topic == "x-rotation" and not(-90 < message < -80)):
            pause_horsti("Die Montagefläche überschreitet die zulässige Neigung ! (5°)")
        elif (topic == "y-rotation" and not(-5 < message < 5)):
            pause_horsti("Die Montagefläche überschreitet die zulässige Neigung ! (5°)")
        elif (topic == "ir_sensor" and message == 1):
            pause_horsti("Die Lichtschranke wurde unterbrochen!")
        print(message)
    except ValueError:
        message = message.payload.decode("utf-8")
        if (topic == "message" and message != "Alles ok!"):
            pause_horsti(message)

def pause_horsti(text):
    try:
        horsti.pause()
        print(time_ns())
    except:
        pass
    window = MainWindow()
    window.message_label.setText(text)
    window.show()
    app.exec()

    if window.everything_ok:
        try:
            horsti.proceed()
        except:
            pass
    else:
        try:
            horsti.abort()
        except:
            pass



app = QApplication(argv)

global window, horsti

while True: 
    try:
        horsti = Horst()
        break
    except: 
        print("I tried to connect to HORST600!")
        sleep(1)

mqtt_client = mqtt.Client("translator")
mqtt_client.connect("192.168.111.62")
mqtt_client.subscribe("temperature")
mqtt_client.subscribe("ir_sensor")
mqtt_client.subscribe("x-rotation")
mqtt_client.subscribe("y-rotation")
mqtt_client.subscribe("message")

mqtt_client.loop_start
mqtt_client.on_message = on_message
mqtt_client.loop_forever()
