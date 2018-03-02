from abc import ABCMeta, abstractmethod
import random

class Environment(object):

    __metaclass__ = ABCMeta

    class ActionSpace(object):

        def __init__(self, as_leng):
            print ("Environment class > ActionSpace")
            self.as_list = range(as_leng)

        def sample(self):
            return random.choice(self.as_list)
            
    
    def __init__(self, as_leng, renderer=None):

        self.as_leng = as_leng
        self.renderer=renderer
        self.episode_number = 0
        self.action_space = self.ActionSpace(as_leng)

    def render(self):
        pass

    @abstractmethod
    def step(self, action):
        """
        RETURN: (observation, reward, done, info)
        """
        raise NotImplementedError("step must be explicitly overridden")

    @abstractmethod
    def reset(self):
        raise NotImplementedError("reset must be explicitly overridden")

