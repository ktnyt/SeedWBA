from abc import ABCMeta, abstractmethod
import random
from environment import Environment


class GridMap(object):

    def __init__(self, agent_pos_default, reward_pos_default):

        self.data = None
        self.ylen = -1
        self.xlen = -1

        self.agent_pos_default = agent_pos_default
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = reward_pos_default
        self.reward_pos = self.reward_pos_default

        self.action_list = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        self.is_reward = False
        self.map_type = 0
        
    def step(self, action):


        """ Wss it rewarding place? """
        if self.is_reward:
            self.reward_pos = [random.randint(1, self.xlen-2),
                               random.randint(1, self.ylen-2), ]
            
        agent_pos_tmp = [x + y for (x, y)
                         in zip(self.agent_pos, self.action_list[action])]

        self.map_type, self.is_reward = self.check(agent_pos_tmp)

        observation = self.data
        reward = 1 if self.is_reward else 0
        done = None
        info = None

        """ Is it wall? """
        if self.map_type == 1:
            return (observation, reward, done, info)

        self.agent_pos = agent_pos_tmp

        return (observation, reward, done, info)
    
    def set(self, map_data, ylen, xlen):

        if len(map_data) != (ylen * xlen):
            print ("ERROR: len(map) != (ylen * xlen)")
            return
            
        self.data = map_data
        self.ylen = ylen
        self.xlen = xlen

    def check(self, agent_pos):
        agent_i = agent_pos[1] * self.xlen + agent_pos[0]
        map_type = self.data[agent_i]
        reward_i = self.reward_pos[1] * self.xlen + self.reward_pos[0]
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

    def __init__(self, agent_pos_default, reward_pos_default, renderer=None):

        super(GridWorldEnv, self).__init__(renderer=renderer, as_leng=4)
        
        self.action_space = self.ActionSpace(self.as_leng)
        self.map = GridMap(agent_pos_default, reward_pos_default)
            
    def step(self, action):
        """
        INPUT: action
        OUTPUT: (observation, reward, done, info)
        """
        
        res = self.map.step(action)
        print (res)
        return res

    def render(self):
        
        print (self.map.reward_pos)
        if self.renderer is not None:
            self.renderer(self.map)

    def reset(self):
        pass
