import time
from image_capture import ImageCapture
from image_classification import ImageClassification

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('model_path', help='requires TeachableMachine savedmodel')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    image_classification = ImageClassification(args.model_path)
    image_classification.loadModel()    
    
    image_capture = ImageCapture()
    time.sleep(2)
    print(image_capture)
    image_capture.captureFrames(image_classification.handleImage)

if __name__ == "__main__":
    main()