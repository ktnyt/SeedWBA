from abc import ABCMeta, abstractmethod
import random
from environment import Environment


class GridMap(object):

    def __init__(self):

        self.data = None
        self.ylen = -1
        self.xlen = -1

        self.agent_pos_default = None
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = None
        self.reward_pos = self.reward_pos_default

        self.action_list = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def step(self, action):

        agent_pos_tmp = [x + y for (x, y)
                         in zip(self.agent_pos, self.action_list[action])]

        map_type, is_reward = self.check(agent_pos_tmp):

        """ Is it wall? """
        if map_type == 1:
            return

        self.agent_pos = agent_pos_tmp
            
    def set(self, map_data, ylen, xlen):

        if len(map) != (ylen * xlen):
            print ("ERROR: len(map) != (ylen * xlen)")
            return
            
        self.data = map_data
        self.ylen = ylen
        self.xlen = xlen

    def check(self, agent_pos):
        agent_i = agent_pos[1] * self.xlen + agent_pos[0]
        map_type = self.data[agent_i]
        reward_i = reward_pos[1] * self.xlen + reward_pos[0]
        is_reward = (reward_i == agent_i)
        return map_type, is_reward

    
class GridWorldEnv(Environment):

    __metaclass__ = ABCMeta

    class ActionSpace(object):

        def __init__(self, as_leng):
            print ("GridWorldEnv class > ActionSpace")            
            self.as_list = range(as_leng)

        def sample(self):
            return random.choice(self.as_list)

    def __init__(self, renderer=None):

        super(GridWorldEnv, self).__init__(renderer=renderer, as_leng=4)
        
        self.action_space = self.ActionSpace(self.as_leng)
        self.map = GridMap()
            
    def step(self, action):
        """
        INPUT: action
        OUTPUT: (observation, reward, done, info)
        """
        self.map.step(action)

        observation = self.map.data
        reward = 0
        done = None
        info = None
        return (observation, reward, done, info)

    def render(self):
        if self.renderer is not None:
            self.renderer(self.map)

    def reset(self):
        pass
