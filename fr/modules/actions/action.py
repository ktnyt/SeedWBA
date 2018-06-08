# -*- coding: utf-8 -*-
class Action(object):
    def __init__(self):
        self.active = False

    def activate(self):
        # Called when action activated
        self.active = True
    
    def update(self):
        # Called every frame while action is activated
        pass

    def deactivate(self):
        # Called when action deactivated
        self.active = False