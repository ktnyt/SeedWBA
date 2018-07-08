# -*- coding: utf-8 -*-
import cv2
import math
from ..analyzers.facedetector import FaceDetector

class Noaction(object):
    def activate(self):
        # Called when action activated
        return {}
    
    def update(self):
        act = {
            "wheelleft": 0.0,
            "wheelright": 0.0
        }
        # Called every frame while action is activated
        if str(FaceDetector.biggestFaceRect) != "None":
            # If face exists
            x, _ = FaceDetector.biggestFaceRectPosNormalized(None)
            size = FaceDetector.biggestFaceSizeNormalized(None)
            if abs(x) > 0.3:
                if x > 0:
                    # Rotate to left
                    act["wheelleft"] -= 0.1
                    act["wheelright"] += 0.1
                else:
                    # Rotate to right
                    act["wheelleft"] += 0.1
                    act["wheelright"] -= 0.1
            if size < 0.1:
                # Move forward
                act["wheelleft"] += 0.1
                act["wheelright"] += 0.1

    def deactivate(self):
        # Called when action deactivated
        return {}