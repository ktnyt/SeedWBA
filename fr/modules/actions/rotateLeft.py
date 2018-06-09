# -*- coding: utf-8 -*-

BASE_ACTION = {
    "armleft": 0.0,
    "armright": 0.0,
    "wheelleft": 0.0,
    "wheelright": 0.0
}

class RotateLeft(object):
    def __init__(self):
        pass

    def activate(self):
        # Called when action activated
        return {}
    
    def update(self):
        # Called every frame while action is activated
        act = BASE_ACTION
        act["wheelleft"] = -0.1
        act["wheelright"] = 0.1
        return act

    def deactivate(self):
        # Called when action deactivated
        return {}
