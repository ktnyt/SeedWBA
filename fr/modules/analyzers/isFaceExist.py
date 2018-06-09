# -*- coding: utf-8 -*-
import cv2
import time
from .facedetector import FaceDetector

class IsFaceExist(object):
    
    def analyze(self, observation):
        facerect = FaceDetector.getFacerect(observation)
        if str(facerect) == "None": return
        return len(facerect)
