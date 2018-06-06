# -*- coding: utf-8 -*-
import cv2

cascade_path = "./haarcascades/haarcascade_frontalface_default.xml"

class FaceDetector(object):
    def __init__(self):
        pass

    def analyze(self, observation):
        # Engray image
        image_gray = cv2.cvtColor(observation["image"], cv2.COLOR_BGR2GRAY)

        # Load cascade classifier
        cascade = cv2.CascadeClassifier(cascade_path)

        # Get facerect
        facerect = cascade.detectMultiScale(
            image_gray, 
            scaleFactor = 1.1,
            minNeighbors = 2,
            minSize = (10, 10)
        )

        if len(facerect) > 0:
            return 1.0
        else:
            return 0.0