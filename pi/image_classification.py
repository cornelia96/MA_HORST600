import tensorflow.keras
import numpy as np
from status_led import StatusLed

class ImageClassification:
    def __init__(self, model_path, status_led, safe_interface):
        self.model_path = model_path
        self.status_led = status_led
        self.safe_interface = safe_interface

    def loadModel(self):
        print('loading model...')
        self.model = tensorflow.keras.models.load_model(self.model_path, compile=False)
        print('model loaded')

    def handleImage(self, data):
        prediction = self.model.predict(data)[0]
        
        print(prediction)

        if prediction[0] > 0.7:
            self.status_led.setStatus(StatusLed.STATUS_OPEN)
            self.safe_interface.open()
        else:
            self.status_led.setStatus(StatusLed.STATUS_CLOSED)
            self.safe_interface.close()
