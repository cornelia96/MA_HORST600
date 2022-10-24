from email import message
import socket, xmlrpc.client, sys
from opcua import Client
from time import sleep
from datetime import datetime
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QWidget
from PyQt6.QtCore import QSize, Qt

# set variable as the ip adress of the opc ua server
SERVER_IP = "XXXX" 
PORTNO = "3470" 
test = "yadayada"

# Class Horst connects to HORST600 and can control the robot
class Horst:
    def __init__(self, user="horstFX", password="WZA3P9", url="192.168.111.62:8080/xml-rpc"):
        self.URL = "@" + url
        '''Username and password (only needed for some calls, including RobotMoveCalls)'''
        self.USERNAME = user
        self.PASSWORD = password
        '''Construct a client with the HorstFX server url, username and password '''
        self.client = xmlrpc.client.ServerProxy("http://" + self.USERNAME + ":" + self.PASSWORD + self.URL)
        print("Initialized xmlrpc client for user '" + self.USERNAME + "'")

    # pause HORST600 movements:
    def pause(self): 
        self.client.HorstFX.Program.pause()

    # check if HORST600 is currently running:
    def isRunning(self):
        self.client.HorstFX.Program.isRunning()

    # abort HORST600 movements:
    def abort(self):
        self.client.HorstFX.Program.abort()

    # continue HORST600 movements:
    def proceed(self):
        self.client.HorstFX.Program.proceed()

# MainWindow() defines the window which opens, when an anomaly is detected by the sensors
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.opcua_client = self.opcua_connect() # initializing opc ua client variable
        self.everything_ok, self.opc_message = self.get_client_variables(opcua_client, 2) # connect to the object variables on the server
        self.everything_ok.set_value(True) # setting default value vor everything_ok
        self.opc_message.set_value("Keine Nachricht!") # setting default value vor opc_message
        self.robi = self.horsti_connect() # connecting to HORST600

        self.setWindowTitle("Fehlermeldung") # setting the title of the window

        # setting the displayed message as the message sent by the opc ua server
        self.message_label = QLabel()
        self.message_label.setText(self.opc_message.get_value())

        # defining the "continue" button
        self.continue_btn = QPushButton("Fortsetzen")
        self.continue_btn.setCheckable(True)
        self.continue_btn.released.connect(self.continue_horst_program)

        #defining the "cancel" button
        self.cancel_btn = QPushButton("Abbrechen")
        self.cancel_btn.setCheckable(True)
        self.cancel_btn.released.connect(self.cancel_horst_program)

        # arranging the window elements
        self.layout = QGridLayout()
        self.layout.addWidget(self.message_label, 0, 0)
        self.layout.addWidget(self.continue_btn, 1, 0)
        self.layout.addWidget(self.cancel_btn, 1, 1)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.container.setFixedSize(400,300)
        self.setCentralWidget(self.container)
    
    # continue_horst_program is called when the user clicks the "continue" button
    def continue_horst_program(self):
        self.robi.proceed() # continue the robots paused movements
        self.everything_ok.set_value(True) # set everything_ok back to default value
        self.opc_message.set_value("Keine Nachricht!") # set opc_message back to default value
        self.hide() # hide window
        while self.everything_ok.get_value(): # program sleeps as long as everything_ok remains True
            sleep(0.001)
        self.robi.pause() # if everything_ok gets set to False again, the robot is paused again...
        self.message_label.setText(self.opc_message.get_value()) # ...the message label is set to the message from the opc ua server again...
        self.show() # ...and the window reappears

    # cancel_horst_program is called when the user clicks the "cancel" button
    def cancel_horst_program(self):
        self.robi.abort() # abort the robots active protocol 
        self.close() # close the window
        pass # restart the script

    # method called to connect to opc ua server
    def opcua_connect(self):
        while True:
            try:
                global opcua_client
                opcua_client = Client(f"opc.tcp://{SERVER_IP}:{PORTNO}") # set up client variable 
                opcua_client.connect() # connect client to server
                print("connected to server")
                return opcua_client 
            except ConnectionRefusedError: # may happen when the server hasn't started running yet
                print(f"{datetime.now()}: I tried to connect to opcua")
                sleep(5) # program waits 5 seconds and tries again

    # method called to connect to HORST600
    def horsti_connect(self):
        while True:
            try:
                robi = Horst() # initialize Horst() variable 
                print("Connected to HORST600") 
                return robi
            except TimeoutError: # may happen when robot isn't connected to the internet or horstFX hasn't started up yet
                print(f"{datetime.now()}: I tried to connect to Horst")
                sleep(5) # program waits 5 seconds and tries again

    # initializing an opc ua client variable
    def get_client_variables(self, opcua_client, client_index): 
        objects = opcua_client.get_objects_node()
        client = objects.get_children()[client_index] 
        return client.get_children()
            
def main(): 
    try: 
        app = QApplication(sys.argv)

        window = MainWindow() # initializing window
        
        while window.everything_ok.get_value(): # as long as everything_ok is True, the program does nothing
            sleep(0.001)

        if window.robi.isRunning(): # checking if robot is currently moving
            window.robi.pause() # pausing the robot
        
        window.show() # showing the window with the error message
        app.exec() # finishing the program if the cancel button is pressed and the program exits 
        
        opcua_client.disconnect() # disconnecting from the opc ua server
        app.quit() # closing the window

    # stopping the program if KeyboardInterrupt is triggered    
    except KeyboardInterrupt:
        try:
            window.opcua_client.disconnect() # disconnecting from the opc ua server if possible
            app.quit()
        except:
            print("Goodbye")

    # closing the program and restarting in case of an unexpected error
    except:
        try:
            window.opcua_client.disconnect()
            app.quit()
            print("error disconnected")
        except:
            print("error Goodbye")


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        pass
