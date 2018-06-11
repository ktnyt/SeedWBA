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

    @classmethod
    def biggestFaceRect(self, observation):
        facerect = self.getFacerect(observation)
        if str(facerect) == "None": return
        return max(facerect, key= (lambda r: r[2] * r[3]))
    
    @classmethod
    def biggestFaceSizeNormalized(self, observation):
        width, height, _ = observation["image"].shape
        biggestface = self.biggestFaceRect(observation)
        if str(biggestface) == "None": return 0.0
        return biggestface[2] * biggestface[3] / width / height

    @classmethod
    def biggestFaceRectPosNormalized(self, observation):
        width, height, _ = observation["image"].shape
        biggestface = self.biggestFaceRect(observation)
        if str(biggestface) == "None": return 0.0, 0.0
        facex = biggestface[0] + biggestface[2] / 2
        facey = biggestface[1] + biggestface[3] / 2
        facexNormalized = (facex / width - 0.5) * 2.0
        faceyNormalized = (facey / height - 0.5) * 2.0
        return facexNormalized, faceyNormalized 