# -*- coding: utf-8 -*-
import cv2
import time

# cascade_path = "./haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "/var/opencv/haarcascades/haarcascade_frontalface_default.xml"

class FaceDetector(object):
    facerect = None
    refreshRate = 0.1 # sec
    lastRefreshed = 0.0 # sec

    @classmethod
    def getFacerect(self, observation):
        # Return cached data or not
        if (time.time() - FaceDetector.lastRefreshed) < FaceDetector.refreshRate or observation == None:
            return FaceDetector.facerect

        # Engray image
        if str(observation["image"]) == "None": return
        image_gray = cv2.cvtColor(observation["image"], cv2.COLOR_BGR2GRAY)

        # Load cascade classifier
        cascade = cv2.CascadeClassifier(cascade_path)

        # Get facerect
        FaceDetector.facerect = cascade.detectMultiScale(
            image_gray, 
            scaleFactor = 1.1,
            minNeighbors = 2,
            minSize = (30, 30)
        )

        # Update cache time
        FaceDetector.lastRefreshed = time.time()

        return FaceDetector.facerect
