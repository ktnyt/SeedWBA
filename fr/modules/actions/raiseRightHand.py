# -*- coding: utf-8 -*-
from .action import Action

BASE_ACTION = {
    "armleft": 0.0,
    "armright": 0.0,
    "headroll": 0.0,
    "headpitch": 0.0,
    "headyaw": 0.0,
    "wheelleft": 0.0,
    "wheelright": 0.0
}

class RaiseRightHand(Action):
    def __init__(self):
        super().__init__()

    def activate(self):
        # Called when action activated
        super().activate()
        act = BASE_ACTION
        act["armright"] = 1.0
        return act
    
    def update(self):
        # Called every frame while action is activated
        super().update()

    def deactivate(self):
        # Called when action deactivated
        super().deactivate()
        return BASE_ACTION
