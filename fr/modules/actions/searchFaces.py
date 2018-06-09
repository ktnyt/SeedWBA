# -*- coding: utf-8 -*-
import time
import math
from ..analyzers.facedetector import FaceDetector

BASE_ACTION = {
    "armleft": 0.0,
    "armright": 0.0,
    "wheelleft": 0.0,
    "wheelright": 0.0
}

class SearchFaces(object):
    def __init__(self):
        pass

    def activate(self):
        # Called when action activated
        return {}
    
    def update(self):
        # Called every frame while action is activated
        facerect = FaceDetector.getFacerect(None)
        act = BASE_ACTION
        if str(facerect) != "None" and len(facerect) > 0:
            act["wheelleft"] = 0.0
            act["wheelright"] = -0.0
        else:
            rectwave = round(math.sin(time.time()))
            act["wheelleft"] = rectwave * 0.1
            act["wheelright"] = -rectwave * 0.1

        return act

    def deactivate(self):
        # Called when action deactivated
        return {}
