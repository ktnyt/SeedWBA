# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Analyzer(object):
    def __init__(self):
        pass

    @abstractmethod
    def analyze(self, observation):
        # Return scholar (not vector or dict)
        return 0;