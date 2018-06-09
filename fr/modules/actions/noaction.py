# -*- coding: utf-8 -*-

class Noaction(object):
    def activate(self):
        # Called when action activated
        return {}
    
    def update(self):
        # Called every frame while action is activated
        return {}

    def deactivate(self):
        # Called when action deactivated
        return {}