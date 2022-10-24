# converting the adc values of the sensor to degree Celsius
def adc_to_celsius(thermistor_value):
  tempC = ((thermistor_value / 5000) * 10000) / (1 - (thermistor_value / 5000))
  tempC = 1 / ((1/298.15) + (1 / 3950.0) * log(tempC / 10000))
  tempC = tempC - 273.15
  return(tempC)
 
# initializing and connecting the MQTT client
client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

# initializing the temperature sensor
thermistor = ADC(Pin(thermistor_pin))
thermistor.atten(ADC.ATTN_11DB)

#initializing the gyroscope/tilt sensor
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))    #initializing the I2C method for ESP32
mpu= mpu6050.accel(i2c)

# reading and publishing the sensor data to the MQTT broker at intervals of 1 ms
while True: 
  tempC = adc_to_celsius(thermistor.read())
  client.publish(TOPIC_TEMP, "{:.2f}".format(tempC))
  xRot, yRot = mpu.get_values()
  client.publish(TOPIC_XROT, "{:.2f}".format(xRot))
  client.publish(TOPIC_YROT, "{:.2f}".format(yRot))
  sleep(0.001)