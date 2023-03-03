# converting the adc values of the sensor to degree Celsius
def adc_to_celsius(thermistor_value):
  tempC = ((thermistor_value / 5000) * 10000) / (1 - (thermistor_value / 5000))
  tempC = 1 / ((1/298.15) + (1 / 3950.0) * log(tempC / 10000))
  tempC = tempC - 273.15
  return(tempC)
 
# initializing and connecting the MQTT client
while True:
  try:
    client = MQTTClient(CLIENT_ID, SERVER)
    client.connect() 
    print("MQTT connection successfull")
    break
  except OSError: # may happen if the MQTT Broker hasn't gone online yet/isn't available
    print("MQTT connect error")
    sleep(1)

# initializing the temperature sensor
thermistor = ADC(Pin(thermistor_pin))
thermistor.atten(ADC.ATTN_11DB)

# initializing the light barrier
distance_sensor = Pin(light_barrier_pin, Pin.IN)

#initializing the gyroscope/tilt sensor
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))    #initializing the I2C method for ESP32
while True:
  try:
    mpu= mpu6050.accel(i2c)
    break
  except OSError: # may happen if the gyroscope isn't connected correctly
    client.publish(TOPIC_MSG, "Der Neigungssensor ist nicht korrekt angeschlossen!")

client.publish(TOPIC_MSG, "Alles ok!")

# reading and publishing the sensor data to the MQTT broker at intervals of 1 ms
while True: 
  try:
    tempC = adc_to_celsius(thermistor.read())
    client.publish(TOPIC_TEMP, "{:.2f}".format(tempC))
    xRot, yRot = mpu.get_values()
    client.publish(TOPIC_XROT, "{:.2f}".format(xRot))
    client.publish(TOPIC_YROT, "{:.2f}".format(yRot))
    client.publish(TOPIC_IR, "{:.2f}".format(yRot))
    sleep(0.001)
  except OSError:
    client.publish(TOPIC_MSG, "Ein oder mehrere Sensoren sind nicht korrekt angeschlossen!")
    sleep(1)