from opcua import Client
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

# constants
TEMP_PIN = 14
LIGHT_BARRIER_1_PIN = 23
LIGHT_BARRIER_2_PIN = 24
LIGHT_BARRIER_3_PIN = 25
LIGHT_BARRIER_4_PIN = 8

#opcua_connect() initializes a Client() variable and attempts to connect to the server
def opcua_connect():
    while True:
        try:
            ip_address = socket.gethostbyname(socket.gethostname() + ".local") # initializing the client variable
            opcua_client = Client(f"opc.tcp://{ip_address}:3470") # since the server and client are both running on the same RPi in this setup, the server endpoint is also the local ip adress
            opcua_client.connect() # connecting to the server
            return opcua_client
        except ConnectionRefusedError:
            print(f"{datetime.now()}: I tried to connect to opcua")
            sleep(5)

# read temperature
def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# convert reading to °C 
def TemperaturAuswertung():
    lines = TemperaturMessung()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
 
def main(): 
    opcua_client = opcua_connect() # initializing opc ua client variable
    objects = opcua_client.get_objects_node() 
    sensor_master = objects.get_children[0] # connect to the sensor_master node on the server
    # connect to the object variables on the server
    temperature = sensor_master.get_children[0] 
    light_gate_1 = sensor_master.get_children[1]
    light_gate_2 = sensor_master.get_children[2]
    light_gate_3 = sensor_master.get_children[3]
    light_gate_4 = sensor_master.get_children[4]
    TemperaturMessung() # blind reading to initialize the sensor
    while True: 
        try: 
            # set client variable values according to the sensor readings
            temperature.set_value(TemperaturAuswertung)
            light_gate_1.set_value(GPIO.input(LIGHT_BARRIER_1_PIN))
            light_gate_2.set_value(GPIO.input(LIGHT_BARRIER_2_PIN))
            light_gate_3.set_value(GPIO.input(LIGHT_BARRIER_3_PIN))
            light_gate_4.set_value(GPIO.input(LIGHT_BARRIER_4_PIN))
            sleep(0.001)

        except KeyboardInterrupt:
            break
    
    opcua_client.disconnect()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM) # set pin numbering mode to BCM (other option is BOARD)
    # set up pins as input pins
    GPIO.setup(TEMP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LIGHT_BARRIER_1_PIN, GPIO.IN)
    GPIO.setup(LIGHT_BARRIER_2_PIN, GPIO.IN)
    GPIO.setup(LIGHT_BARRIER_3_PIN, GPIO.IN)
    GPIO.setup(LIGHT_BARRIER_4_PIN, GPIO.IN)

    #preparations for the temp sensor
    base_dir = '/sys/bus/w1/devices/'
    while True:
        try:
            device_folder = glob.glob(base_dir + '28*')[0]
            break
        except IndexError:
            sleep(1)
            continue
    device_file = device_folder + '/w1_slave'

    main()