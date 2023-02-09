from PIL import Image, ImageOps
import numpy as np

import io
import time
import picamera

class ImageCapture:

    def __init__(self):
        self.stream = io.BytesIO()
        self.camera = picamera.PiCamera()
        self.camera.start_preview()
        
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

    def cleanup(self, type, value, traceback):
        self.camera.close()
        self.stream.close()

    def captureFrames(self, callback):
        print('start camera')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        for current_capture in self.camera.capture_continuous(self.stream, format='jpeg'):
                # Rewind the stream and send the image data over the wire
                self.stream.seek(0)

                image = Image.open(self.stream)
        
                #resize the image to a 224x224 with the same strategy as in TM2:
                #resizing the image to be at least 224x224 and then cropping from the center
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)

                #turn the image into a numpy array
                image_array = np.asarray(image)
                
                # Reset the stream for the next capture
                self.stream.seek(0)
                self.stream.truncate()

                # Normalize the image
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

                # Load the image into the array
                data[0] = normalized_image_array

                callback(data)