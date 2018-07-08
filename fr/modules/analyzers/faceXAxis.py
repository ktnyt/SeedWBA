# -*- coding: utf-8 -*-
import cv2
from .facedetector import FaceDetector

class FaceXAxis(object):
    
    def analyze(self, observation):
        x, _ = FaceDetector.biggestFaceRectPosNormalized(observation)
        return x
