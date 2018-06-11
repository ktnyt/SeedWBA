# -*- coding: utf-8 -*-
import cv2
from .facedetector import FaceDetector

class FaceYAxis(object):
    
    def analyze(self, observation):
        _, y = FaceDetector.biggestFaceRectPosNormalized(observation)
        return y
